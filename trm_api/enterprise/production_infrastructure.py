"""
Production Infrastructure for TRM-OS

Enterprise-grade logging, caching, and monitoring infrastructure
for production deployments with high availability and scalability.
"""

from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic
import logging
import asyncio
import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import redis.asyncio as redis
from redis.asyncio import Redis
import structlog
from structlog import get_logger
import aiofiles
import gzip
from contextlib import asynccontextmanager
import uuid
from collections import defaultdict, deque
import traceback

T = TypeVar('T')

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


class LogLevel(str, Enum):
    """Log levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CacheStrategy(str, Enum):
    """Cache strategies"""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: datetime
    level: LogLevel
    message: str
    logger_name: str
    module: str
    function: str
    line_number: int
    context: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    execution_time_ms: Optional[float] = None
    error_details: Optional[Dict[str, Any]] = None


@dataclass
class CacheEntry(Generic[T]):
    """Cache entry with metadata"""
    key: str
    value: T
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    ttl_seconds: Optional[int] = None
    tags: List[str] = field(default_factory=list)
    size_bytes: int = 0
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if not self.ttl_seconds:
            return False
        return (datetime.now() - self.created_at).total_seconds() > self.ttl_seconds
    
    def should_evict(self, strategy: CacheStrategy) -> bool:
        """Check if entry should be evicted based on strategy"""
        if self.is_expired():
            return True
        
        # Additional strategy-specific logic would go here
        return False


@dataclass
class MetricEntry:
    """Performance metric entry"""
    metric_name: str
    value: Union[int, float]
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metric_type: str = "gauge"  # gauge, counter, histogram


class ProductionLogger:
    """
    Enterprise Production Logger
    
    Features:
    - Structured JSON logging
    - Distributed tracing
    - Log aggregation and rotation
    - Performance metrics
    - Error tracking and alerting
    - Context-aware logging
    """
    
    def __init__(
        self,
        service_name: str = "trm-os",
        log_level: LogLevel = LogLevel.INFO,
        log_file: Optional[str] = None,
        enable_compression: bool = True,
        max_file_size_mb: int = 100,
        max_files: int = 10
    ):
        self.service_name = service_name
        self.log_level = log_level
        self.log_file = log_file
        self.enable_compression = enable_compression
        self.max_file_size_mb = max_file_size_mb
        self.max_files = max_files
        
        # Initialize structured logger
        self.logger = get_logger(service_name)
        
        # Performance tracking
        self._log_count = defaultdict(int)
        self._error_count = 0
        self._performance_metrics = deque(maxlen=1000)
        
        # Context tracking
        self._active_traces: Dict[str, Dict[str, Any]] = {}
        self._current_context = {}
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Configure standard logging
        logging.basicConfig(
            level=getattr(logging, self.log_level.upper()),
            format='%(message)s'  # structlog handles formatting
        )
        
        if self.log_file:
            # Setup file rotation
            from logging.handlers import RotatingFileHandler
            handler = RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_file_size_mb * 1024 * 1024,
                backupCount=self.max_files
            )
            logging.getLogger().addHandler(handler)
    
    # ================================
    # CONTEXT MANAGEMENT
    # ================================
    
    @asynccontextmanager
    async def trace_context(
        self,
        operation: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **context
    ):
        """Create tracing context for operation"""
        trace_id = str(uuid.uuid4())
        start_time = time.time()
        
        trace_context = {
            'trace_id': trace_id,
            'operation': operation,
            'user_id': user_id,
            'agent_id': agent_id,
            'session_id': session_id,
            'start_time': start_time,
            **context
        }
        
        self._active_traces[trace_id] = trace_context
        
        # Bind context to logger
        bound_logger = self.logger.bind(
            trace_id=trace_id,
            operation=operation,
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id
        )
        
        try:
            bound_logger.info("Operation started", **context)
            yield trace_id, bound_logger
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            bound_logger.error(
                "Operation failed",
                error=str(e),
                error_type=type(e).__name__,
                execution_time_ms=execution_time,
                traceback=traceback.format_exc()
            )
            self._error_count += 1
            raise
            
        finally:
            execution_time = (time.time() - start_time) * 1000
            bound_logger.info(
                "Operation completed",
                execution_time_ms=execution_time
            )
            
            # Record performance metric
            self._performance_metrics.append(MetricEntry(
                metric_name=f"operation.{operation}.duration",
                value=execution_time,
                timestamp=datetime.now(),
                tags={'operation': operation, 'user_id': user_id or 'unknown'}
            ))
            
            # Cleanup trace
            if trace_id in self._active_traces:
                del self._active_traces[trace_id]
    
    def set_context(self, **context):
        """Set global context for subsequent logs"""
        self._current_context.update(context)
    
    def clear_context(self):
        """Clear global context"""
        self._current_context.clear()
    
    # ================================
    # LOGGING METHODS
    # ================================
    
    def debug(self, message: str, **context):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, **context)
    
    def info(self, message: str, **context):
        """Log info message"""
        self._log(LogLevel.INFO, message, **context)
    
    def warning(self, message: str, **context):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, **context)
    
    def error(self, message: str, error: Optional[Exception] = None, **context):
        """Log error message"""
        if error:
            context.update({
                'error': str(error),
                'error_type': type(error).__name__,
                'traceback': traceback.format_exc()
            })
        self._log(LogLevel.ERROR, message, **context)
        self._error_count += 1
    
    def critical(self, message: str, error: Optional[Exception] = None, **context):
        """Log critical message"""
        if error:
            context.update({
                'error': str(error),
                'error_type': type(error).__name__,
                'traceback': traceback.format_exc()
            })
        self._log(LogLevel.CRITICAL, message, **context)
        self._error_count += 1
    
    def _log(self, level: LogLevel, message: str, **context):
        """Internal logging method"""
        # Merge contexts
        full_context = {**self._current_context, **context}
        
        # Get bound logger with context
        bound_logger = self.logger.bind(**full_context)
        
        # Log with appropriate level
        getattr(bound_logger, level.value)(message)
        
        # Track log counts
        self._log_count[level] += 1
    
    # ================================
    # METRICS AND MONITORING
    # ================================
    
    def record_metric(
        self,
        metric_name: str,
        value: Union[int, float],
        metric_type: str = "gauge",
        **tags
    ):
        """Record performance metric"""
        metric = MetricEntry(
            metric_name=metric_name,
            value=value,
            timestamp=datetime.now(),
            tags=tags,
            metric_type=metric_type
        )
        self._performance_metrics.append(metric)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        recent_metrics = list(self._performance_metrics)
        
        return {
            'log_counts': dict(self._log_count),
            'error_count': self._error_count,
            'active_traces': len(self._active_traces),
            'recent_metrics_count': len(recent_metrics),
            'avg_operation_time': self._calculate_avg_operation_time(recent_metrics)
        }
    
    def _calculate_avg_operation_time(self, metrics: List[MetricEntry]) -> float:
        """Calculate average operation time from metrics"""
        duration_metrics = [
            m for m in metrics 
            if 'duration' in m.metric_name
        ]
        
        if not duration_metrics:
            return 0.0
        
        total_time = sum(m.value for m in duration_metrics)
        return total_time / len(duration_metrics)


class ProductionCache:
    """
    Enterprise Production Cache
    
    Features:
    - Redis-based distributed caching
    - Multiple eviction strategies
    - Cache warming and preloading
    - Performance monitoring
    - TTL management
    - Tag-based invalidation
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        default_ttl: int = 3600,  # 1 hour
        max_memory_mb: int = 512,
        eviction_policy: str = "allkeys-lru",
        key_prefix: str = "trm-os:"
    ):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.max_memory_mb = max_memory_mb
        self.eviction_policy = eviction_policy
        self.key_prefix = key_prefix
        
        # Redis connection
        self._redis: Optional[Redis] = None
        
        # Performance tracking
        self._hit_count = 0
        self._miss_count = 0
        self._set_count = 0
        self._delete_count = 0
        
        # Local cache for frequently accessed data
        self._local_cache: Dict[str, CacheEntry] = {}
        self._local_cache_max_size = 1000
        
        self.logger = get_logger("cache")
    
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self._redis = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            await self._redis.ping()
            
            # Configure Redis memory settings
            await self._redis.config_set("maxmemory", f"{self.max_memory_mb}mb")
            await self._redis.config_set("maxmemory-policy", self.eviction_policy)
            
            self.logger.info("Redis cache initialized", redis_url=self.redis_url)
            
        except Exception as e:
            self.logger.error("Failed to initialize Redis cache", error=str(e))
            # Fall back to local cache only
            self._redis = None
    
    async def close(self):
        """Close Redis connection"""
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    # ================================
    # CACHE OPERATIONS
    # ================================
    
    async def get(self, key: str, default=None) -> Any:
        """Get value from cache"""
        full_key = self._make_key(key)
        
        # Try local cache first
        if full_key in self._local_cache:
            entry = self._local_cache[full_key]
            if not entry.is_expired():
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                self._hit_count += 1
                return entry.value
            else:
                # Remove expired entry
                del self._local_cache[full_key]
        
        # Try Redis cache
        if self._redis:
            try:
                value = await self._redis.get(full_key)
                if value is not None:
                    # Deserialize value
                    deserialized = self._deserialize(value)
                    
                    # Update local cache
                    self._update_local_cache(full_key, deserialized)
                    
                    self._hit_count += 1
                    return deserialized
            except Exception as e:
                self.logger.error("Redis get failed", key=key, error=str(e))
        
        self._miss_count += 1
        return default
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Set value in cache"""
        full_key = self._make_key(key)
        ttl = ttl or self.default_ttl
        tags = tags or []
        
        # Serialize value
        serialized = self._serialize(value)
        
        # Update local cache
        self._update_local_cache(full_key, value, ttl, tags)
        
        # Update Redis cache
        if self._redis:
            try:
                await self._redis.setex(full_key, ttl, serialized)
                
                # Store tags for invalidation
                if tags:
                    for tag in tags:
                        await self._redis.sadd(f"tag:{tag}", full_key)
                        await self._redis.expire(f"tag:{tag}", ttl)
                
                self._set_count += 1
                return True
                
            except Exception as e:
                self.logger.error("Redis set failed", key=key, error=str(e))
        
        return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        full_key = self._make_key(key)
        
        # Remove from local cache
        if full_key in self._local_cache:
            del self._local_cache[full_key]
        
        # Remove from Redis
        if self._redis:
            try:
                result = await self._redis.delete(full_key)
                self._delete_count += 1
                return result > 0
            except Exception as e:
                self.logger.error("Redis delete failed", key=key, error=str(e))
        
        return False
    
    async def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all cache entries with specific tag"""
        if not self._redis:
            return 0
        
        try:
            # Get all keys with this tag
            keys = await self._redis.smembers(f"tag:{tag}")
            
            if keys:
                # Delete all keys
                deleted = await self._redis.delete(*keys)
                
                # Remove from local cache
                for key in keys:
                    if key in self._local_cache:
                        del self._local_cache[key]
                
                # Clean up tag set
                await self._redis.delete(f"tag:{tag}")
                
                self.logger.info("Invalidated cache by tag", tag=tag, count=deleted)
                return deleted
            
            return 0
            
        except Exception as e:
            self.logger.error("Tag invalidation failed", tag=tag, error=str(e))
            return 0
    
    async def clear_all(self) -> bool:
        """Clear all cache entries"""
        # Clear local cache
        self._local_cache.clear()
        
        # Clear Redis cache
        if self._redis:
            try:
                await self._redis.flushdb()
                self.logger.info("Cache cleared")
                return True
            except Exception as e:
                self.logger.error("Cache clear failed", error=str(e))
        
        return False
    
    # ================================
    # CACHE WARMING AND PRELOADING
    # ================================
    
    async def warm_cache(self, warming_func: Callable, keys: List[str]):
        """Warm cache with precomputed values"""
        self.logger.info("Starting cache warming", key_count=len(keys))
        
        start_time = time.time()
        warmed = 0
        
        for key in keys:
            try:
                # Check if already cached
                if await self.get(key) is None:
                    # Compute and cache value
                    value = await warming_func(key)
                    if value is not None:
                        await self.set(key, value)
                        warmed += 1
                        
            except Exception as e:
                self.logger.error("Cache warming failed for key", key=key, error=str(e))
        
        duration = time.time() - start_time
        self.logger.info(
            "Cache warming completed",
            warmed=warmed,
            total=len(keys),
            duration_seconds=duration
        )
    
    # ================================
    # UTILITY METHODS
    # ================================
    
    def _make_key(self, key: str) -> str:
        """Create full cache key with prefix"""
        return f"{self.key_prefix}{key}"
    
    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        try:
            return json.dumps(value, default=str)
        except Exception:
            # Fall back to string representation
            return str(value)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            return json.loads(value)
        except Exception:
            # Return as string if JSON parsing fails
            return value
    
    def _update_local_cache(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None
    ):
        """Update local cache with size management"""
        # Remove expired entries
        self._cleanup_local_cache()
        
        # Evict entries if cache is full
        if len(self._local_cache) >= self._local_cache_max_size:
            self._evict_local_cache_entries()
        
        # Create cache entry
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            ttl_seconds=ttl,
            tags=tags or [],
            size_bytes=len(str(value))
        )
        
        self._local_cache[key] = entry
    
    def _cleanup_local_cache(self):
        """Remove expired entries from local cache"""
        expired_keys = [
            key for key, entry in self._local_cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self._local_cache[key]
    
    def _evict_local_cache_entries(self):
        """Evict entries from local cache using LRU strategy"""
        if not self._local_cache:
            return
        
        # Sort by last accessed time
        sorted_entries = sorted(
            self._local_cache.items(),
            key=lambda x: x[1].last_accessed
        )
        
        # Remove oldest 10% of entries
        evict_count = max(1, len(sorted_entries) // 10)
        for i in range(evict_count):
            key = sorted_entries[i][0]
            del self._local_cache[key]
    
    # ================================
    # MONITORING AND METRICS
    # ================================
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self._hit_count + self._miss_count
        hit_rate = (self._hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_count': self._hit_count,
            'miss_count': self._miss_count,
            'hit_rate_percent': round(hit_rate, 2),
            'set_count': self._set_count,
            'delete_count': self._delete_count,
            'local_cache_size': len(self._local_cache),
            'redis_connected': self._redis is not None
        }
    
    async def get_redis_info(self) -> Dict[str, Any]:
        """Get Redis server information"""
        if not self._redis:
            return {'error': 'Redis not connected'}
        
        try:
            info = await self._redis.info()
            return {
                'memory_used': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits'),
                'keyspace_misses': info.get('keyspace_misses')
            }
        except Exception as e:
            return {'error': str(e)}


# Global instances
production_logger = ProductionLogger()
production_cache = ProductionCache()


# Decorator for automatic caching
def cached(ttl: int = 3600, tags: Optional[List[str]] = None):
    """Decorator for automatic function result caching"""
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_data = {
                'function': func.__name__,
                'args': args,
                'kwargs': kwargs
            }
            cache_key = hashlib.md5(
                json.dumps(key_data, sort_keys=True, default=str).encode()
            ).hexdigest()
            
            # Try to get from cache
            cached_result = await production_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await production_cache.set(cache_key, result, ttl=ttl, tags=tags)
            
            return result
        
        return wrapper
    return decorator


# Context manager for performance logging
@asynccontextmanager
async def log_performance(operation: str, **context):
    """Context manager for automatic performance logging"""
    async with production_logger.trace_context(operation, **context) as (trace_id, logger):
        yield logger 