#!/usr/bin/env python3
"""
DataSensingAgent - TRM-OS v2.0 Living System

Auto-triggering agent cho file changes với semantic analysis.
Implements real-time monitoring của data changes và triggers
appropriate knowledge evolution processes.

Key Capabilities:
- File system watching với real-time detection
- Auto-triggering của knowledge evolution
- Semantic difference analysis
- Integration với Living Knowledge Core
- Cross-platform file monitoring

Philosophy: Agent as "enzyme của hệ tiêu hóa" - tự động phát hiện và xử lý changes
"""

import asyncio
import os
import time
import hashlib
import logging
from typing import Dict, List, Optional, Any, Set, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from pathlib import Path
import json
import threading
from concurrent.futures import ThreadPoolExecutor

# Platform-specific imports
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    logger.warning("Watchdog not available, falling back to polling")

from trm_api.core.logging_config import get_logger
from trm_api.core.living_knowledge_core import get_living_knowledge_core, LivingKnowledgeCore
from trm_api.core.semantic_change_detector import get_semantic_change_detector, SemanticChangeDetector
from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType
from trm_api.agents.base_agent import BaseAgent

logger = get_logger(__name__)


class FileChangeType(str, Enum):
    """Types of file changes detected"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"
    RENAMED = "renamed"


class WatchMode(str, Enum):
    """File watching modes"""
    REAL_TIME = "real_time"      # Watchdog-based real-time monitoring
    POLLING = "polling"          # Polling-based monitoring
    HYBRID = "hybrid"            # Combination of both


@dataclass
class FileChangeEvent:
    """File change event với metadata"""
    file_path: str
    change_type: FileChangeType
    timestamp: datetime
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    old_path: Optional[str] = None  # For moves/renames
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WatchedPath:
    """Configuration cho watched path"""
    path: str
    recursive: bool = True
    file_patterns: List[str] = field(default_factory=lambda: ["*.md", "*.txt", "*.json", "*.py"])
    ignore_patterns: List[str] = field(default_factory=lambda: ["*.tmp", "*.log", "__pycache__", ".git"])
    auto_trigger: bool = True
    semantic_analysis: bool = True


@dataclass
class ProcessingQueue:
    """Queue cho file change processing"""
    pending_changes: List[FileChangeEvent] = field(default_factory=list)
    processing_changes: Set[str] = field(default_factory=set)
    max_queue_size: int = 100
    batch_size: int = 5
    processing_delay: float = 1.0  # Delay để avoid rapid fire changes


class FileSystemWatcher:
    """
    Cross-platform file system watcher với real-time và polling support
    """
    
    def __init__(self, data_sensing_agent: 'DataSensingAgent'):
        self.agent = data_sensing_agent
        self.watch_mode = WatchMode.HYBRID if WATCHDOG_AVAILABLE else WatchMode.POLLING
        self.observer: Optional[Observer] = None
        self.polling_thread: Optional[threading.Thread] = None
        self.is_watching = False
        self.file_states: Dict[str, Dict[str, Any]] = {}  # Track file states cho polling
        self.last_poll_time = datetime.now()
        
        logger.info(f"FileSystemWatcher initialized with mode: {self.watch_mode}")
    
    async def start_watching(self, watched_paths: List[WatchedPath]) -> bool:
        """Start file system watching"""
        try:
            if self.is_watching:
                logger.warning("File system watcher already running")
                return True
            
            if self.watch_mode in [WatchMode.REAL_TIME, WatchMode.HYBRID] and WATCHDOG_AVAILABLE:
                await self._start_watchdog_monitoring(watched_paths)
            
            if self.watch_mode in [WatchMode.POLLING, WatchMode.HYBRID]:
                await self._start_polling_monitoring(watched_paths)
            
            self.is_watching = True
            logger.info("File system watching started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting file system watcher: {e}")
            return False
    
    async def _start_watchdog_monitoring(self, watched_paths: List[WatchedPath]) -> None:
        """Start watchdog-based real-time monitoring"""
        try:
            self.observer = Observer()
            
            for watched_path in watched_paths:
                if os.path.exists(watched_path.path):
                    event_handler = TRMFileSystemEventHandler(self.agent, watched_path)
                    self.observer.schedule(
                        event_handler, 
                        watched_path.path, 
                        recursive=watched_path.recursive
                    )
                    logger.info(f"Watching path with watchdog: {watched_path.path}")
                else:
                    logger.warning(f"Watched path does not exist: {watched_path.path}")
            
            self.observer.start()
            logger.info("Watchdog monitoring started")
            
        except Exception as e:
            logger.error(f"Error starting watchdog monitoring: {e}")
    
    async def _start_polling_monitoring(self, watched_paths: List[WatchedPath]) -> None:
        """Start polling-based monitoring"""
        try:
            # Initialize file states
            for watched_path in watched_paths:
                await self._scan_initial_state(watched_path)
            
            # Start polling thread
            self.polling_thread = threading.Thread(
                target=self._polling_worker,
                args=(watched_paths,),
                daemon=True
            )
            self.polling_thread.start()
            
            logger.info("Polling monitoring started")
            
        except Exception as e:
            logger.error(f"Error starting polling monitoring: {e}")
    
    async def _scan_initial_state(self, watched_path: WatchedPath) -> None:
        """Scan initial state của files để establish baseline"""
        try:
            path = Path(watched_path.path)
            
            if not path.exists():
                return
            
            if path.is_file():
                await self._record_file_state(str(path))
            else:
                # Scan directory
                for file_path in path.rglob("*"):
                    if file_path.is_file() and self._should_monitor_file(str(file_path), watched_path):
                        await self._record_file_state(str(file_path))
            
            logger.debug(f"Initial state scanned for: {watched_path.path}")
            
        except Exception as e:
            logger.error(f"Error scanning initial state: {e}")
    
    async def _record_file_state(self, file_path: str) -> None:
        """Record current state của file"""
        try:
            stat = os.stat(file_path)
            
            # Calculate file hash for change detection
            file_hash = await self._calculate_file_hash(file_path)
            
            self.file_states[file_path] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "hash": file_hash,
                "last_checked": time.time()
            }
            
        except Exception as e:
            logger.debug(f"Error recording file state for {file_path}: {e}")
    
    async def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate hash của file content"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.debug(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _polling_worker(self, watched_paths: List[WatchedPath]) -> None:
        """Polling worker thread"""
        while self.is_watching:
            try:
                current_time = time.time()
                
                for watched_path in watched_paths:
                    asyncio.run(self._poll_path_changes(watched_path))
                
                # Sleep before next poll
                time.sleep(2.0)  # Poll every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in polling worker: {e}")
                time.sleep(5.0)  # Longer sleep on error
    
    async def _poll_path_changes(self, watched_path: WatchedPath) -> None:
        """Poll for changes in một specific path"""
        try:
            path = Path(watched_path.path)
            
            if not path.exists():
                return
            
            current_files = set()
            
            if path.is_file():
                if self._should_monitor_file(str(path), watched_path):
                    current_files.add(str(path))
                    await self._check_file_changes(str(path))
            else:
                # Check directory
                for file_path in path.rglob("*"):
                    if file_path.is_file() and self._should_monitor_file(str(file_path), watched_path):
                        current_files.add(str(file_path))
                        await self._check_file_changes(str(file_path))
            
            # Check for deleted files
            tracked_files = set(
                fp for fp in self.file_states.keys() 
                if fp.startswith(str(path))
            )
            deleted_files = tracked_files - current_files
            
            for deleted_file in deleted_files:
                await self._handle_file_deleted(deleted_file)
                del self.file_states[deleted_file]
            
        except Exception as e:
            logger.error(f"Error polling path changes: {e}")
    
    async def _check_file_changes(self, file_path: str) -> None:
        """Check if file has changed"""
        try:
            if not os.path.exists(file_path):
                return
            
            stat = os.stat(file_path)
            current_hash = await self._calculate_file_hash(file_path)
            
            if file_path in self.file_states:
                # File exists in state, check for changes
                old_state = self.file_states[file_path]
                
                if (stat.st_mtime != old_state["mtime"] or 
                    stat.st_size != old_state["size"] or 
                    current_hash != old_state["hash"]):
                    
                    # File has changed
                    await self._handle_file_modified(file_path, stat.st_size, current_hash)
                    
                    # Update state
                    self.file_states[file_path] = {
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "hash": current_hash,
                        "last_checked": time.time()
                    }
            else:
                # New file
                await self._handle_file_created(file_path, stat.st_size, current_hash)
                
                # Record state
                self.file_states[file_path] = {
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "hash": current_hash,
                    "last_checked": time.time()
                }
            
        except Exception as e:
            logger.debug(f"Error checking file changes for {file_path}: {e}")
    
    def _should_monitor_file(self, file_path: str, watched_path: WatchedPath) -> bool:
        """Check if file should be monitored"""
        file_name = os.path.basename(file_path)
        
        # Check ignore patterns
        for ignore_pattern in watched_path.ignore_patterns:
            if ignore_pattern.replace("*", "") in file_path:
                return False
        
        # Check file patterns
        if watched_path.file_patterns:
            for pattern in watched_path.file_patterns:
                if pattern == "*" or pattern.replace("*", "") in file_name:
                    return True
            return False
        
        return True
    
    async def _handle_file_created(self, file_path: str, file_size: int, file_hash: str) -> None:
        """Handle file creation event"""
        event = FileChangeEvent(
            file_path=file_path,
            change_type=FileChangeType.CREATED,
            timestamp=datetime.now(),
            file_size=file_size,
            file_hash=file_hash
        )
        await self.agent.handle_file_change(event)
    
    async def _handle_file_modified(self, file_path: str, file_size: int, file_hash: str) -> None:
        """Handle file modification event"""
        event = FileChangeEvent(
            file_path=file_path,
            change_type=FileChangeType.MODIFIED,
            timestamp=datetime.now(),
            file_size=file_size,
            file_hash=file_hash
        )
        await self.agent.handle_file_change(event)
    
    async def _handle_file_deleted(self, file_path: str) -> None:
        """Handle file deletion event"""
        event = FileChangeEvent(
            file_path=file_path,
            change_type=FileChangeType.DELETED,
            timestamp=datetime.now()
        )
        await self.agent.handle_file_change(event)
    
    async def stop_watching(self) -> None:
        """Stop file system watching"""
        try:
            self.is_watching = False
            
            if self.observer:
                self.observer.stop()
                self.observer.join()
                self.observer = None
            
            if self.polling_thread:
                self.polling_thread.join(timeout=5.0)
                self.polling_thread = None
            
            logger.info("File system watching stopped")
            
        except Exception as e:
            logger.error(f"Error stopping file system watcher: {e}")


class TRMFileSystemEventHandler(FileSystemEventHandler):
    """Watchdog event handler cho TRM-OS"""
    
    def __init__(self, agent: 'DataSensingAgent', watched_path: WatchedPath):
        super().__init__()
        self.agent = agent
        self.watched_path = watched_path
    
    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle any file system event"""
        if event.is_directory:
            return
        
        # Check if file should be monitored
        if not self.agent.watcher._should_monitor_file(event.src_path, self.watched_path):
            return
        
        # Create file change event
        change_type = self._map_event_type(event.event_type)
        
        file_event = FileChangeEvent(
            file_path=event.src_path,
            change_type=change_type,
            timestamp=datetime.now(),
            old_path=getattr(event, 'dest_path', None)
        )
        
        # Handle event asynchronously
        asyncio.create_task(self.agent.handle_file_change(file_event))
    
    def _map_event_type(self, event_type: str) -> FileChangeType:
        """Map watchdog event type to FileChangeType"""
        mapping = {
            "created": FileChangeType.CREATED,
            "modified": FileChangeType.MODIFIED,
            "deleted": FileChangeType.DELETED,
            "moved": FileChangeType.MOVED
        }
        return mapping.get(event_type, FileChangeType.MODIFIED)


class DataSensingAgent(BaseAgent):
    """
    DataSensingAgent - Auto-triggering agent cho content changes
    
    Key responsibilities:
    - Monitor file system changes real-time
    - Auto-trigger knowledge evolution processes  
    - Perform semantic difference analysis
    - Coordinate với Living Knowledge Core
    - Manage processing queues và batching
    
    Philosophy: Agent as "enzyme của hệ tiêu hóa" - automatically detect và process changes
    """
    
    def __init__(self, agent_id: str = "data_sensing_agent"):
        super().__init__(
            agent_id=agent_id,
            agent_type="data_sensing",
            capabilities=["file_monitoring", "semantic_analysis", "auto_triggering"]
        )
        
        # Core components
        self.living_knowledge_core: Optional[LivingKnowledgeCore] = None
        self.semantic_detector: Optional[SemanticChangeDetector] = None
        self.watcher = FileSystemWatcher(self)
        self.event_bus = SystemEventBus()
        
        # Configuration
        self.config = {
            "auto_trigger_enabled": True,
            "semantic_analysis_enabled": True,
            "batch_processing": True,
            "processing_delay": 2.0,  # Wait 2s after change để avoid rapid updates
            "max_queue_size": 50,
            "concurrent_processing": 3
        }
        
        # State management
        self.watched_paths: List[WatchedPath] = []
        self.processing_queue = ProcessingQueue()
        self.is_running = False
        self.processing_task: Optional[asyncio.Task] = None
        self.file_content_cache: Dict[str, str] = {}
        
        # Statistics
        self.stats = {
            "files_monitored": 0,
            "changes_detected": 0,
            "evolutions_triggered": 0,
            "semantic_analyses_performed": 0,
            "errors_encountered": 0
        }
        
        logger.info(f"DataSensingAgent {agent_id} initialized")
    
    async def initialize(self) -> bool:
        """Initialize DataSensingAgent"""
        try:
            # Get core components
            self.living_knowledge_core = await get_living_knowledge_core()
            self.semantic_detector = get_semantic_change_detector()
            
            # Set default watched paths
            self.watched_paths = [
                WatchedPath(
                    path="docs/",
                    recursive=True,
                    file_patterns=["*.md", "*.txt"],
                    auto_trigger=True,
                    semantic_analysis=True
                ),
                WatchedPath(
                    path="trm_api/",
                    recursive=True,
                    file_patterns=["*.py"],
                    auto_trigger=True,
                    semantic_analysis=False  # Code changes handled differently
                )
            ]
            
            self.is_initialized = True
            logger.info("DataSensingAgent initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing DataSensingAgent: {e}")
            return False
    
    async def start_monitoring(self) -> bool:
        """Start file system monitoring"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if self.is_running:
                logger.warning("DataSensingAgent already running")
                return True
            
            # Start file system watcher
            success = await self.watcher.start_watching(self.watched_paths)
            if not success:
                return False
            
            # Start processing queue worker
            self.processing_task = asyncio.create_task(self._process_queue_worker())
            
            self.is_running = True
            logger.info("DataSensingAgent monitoring started")
            
            # Publish startup event
            await self.event_bus.publish(SystemEvent(
                event_type="agent.data_sensing.started",
                entity_id=self.agent_id,
                data={"watched_paths_count": len(self.watched_paths)}
            ))
            
            return True
            
        except Exception as e:
            logger.error(f"Error starting DataSensingAgent monitoring: {e}")
            return False
    
    async def handle_file_change(self, event: FileChangeEvent) -> None:
        """Handle file change event"""
        try:
            logger.debug(f"File change detected: {event.change_type} - {event.file_path}")
            
            self.stats["changes_detected"] += 1
            
            # Add to processing queue
            if len(self.processing_queue.pending_changes) < self.config["max_queue_size"]:
                self.processing_queue.pending_changes.append(event)
            else:
                logger.warning("Processing queue full, dropping oldest event")
                self.processing_queue.pending_changes.pop(0)
                self.processing_queue.pending_changes.append(event)
            
        except Exception as e:
            logger.error(f"Error handling file change: {e}")
            self.stats["errors_encountered"] += 1
    
    async def _process_queue_worker(self) -> None:
        """Background worker để process file change queue"""
        while self.is_running:
            try:
                if not self.processing_queue.pending_changes:
                    await asyncio.sleep(0.5)
                    continue
                
                # Get batch of changes to process
                batch_size = min(
                    len(self.processing_queue.pending_changes),
                    self.processing_queue.batch_size
                )
                
                batch = self.processing_queue.pending_changes[:batch_size]
                self.processing_queue.pending_changes = self.processing_queue.pending_changes[batch_size:]
                
                # Process batch
                await self._process_change_batch(batch)
                
                # Delay between batches
                await asyncio.sleep(self.processing_queue.processing_delay)
                
            except Exception as e:
                logger.error(f"Error in queue worker: {e}")
                self.stats["errors_encountered"] += 1
                await asyncio.sleep(5.0)  # Longer sleep on error
    
    async def _process_change_batch(self, batch: List[FileChangeEvent]) -> None:
        """Process batch of file changes"""
        try:
            # Group changes by file để avoid duplicate processing
            file_changes = {}
            for event in batch:
                file_path = event.file_path
                if file_path not in file_changes or event.timestamp > file_changes[file_path].timestamp:
                    file_changes[file_path] = event
            
            # Process each unique file change
            semaphore = asyncio.Semaphore(self.config["concurrent_processing"])
            tasks = [
                self._process_single_change(event, semaphore)
                for event in file_changes.values()
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"Error processing change batch: {e}")
            self.stats["errors_encountered"] += 1
    
    async def _process_single_change(self, event: FileChangeEvent, semaphore: asyncio.Semaphore) -> None:
        """Process single file change event"""
        async with semaphore:
            try:
                file_path = event.file_path
                
                # Skip if already processing
                if file_path in self.processing_queue.processing_changes:
                    return
                
                self.processing_queue.processing_changes.add(file_path)
                
                try:
                    # Handle different change types
                    if event.change_type == FileChangeType.DELETED:
                        await self._handle_file_deletion(event)
                    elif event.change_type in [FileChangeType.CREATED, FileChangeType.MODIFIED]:
                        await self._handle_file_content_change(event)
                    elif event.change_type in [FileChangeType.MOVED, FileChangeType.RENAMED]:
                        await self._handle_file_move(event)
                
                finally:
                    self.processing_queue.processing_changes.discard(file_path)
                
            except Exception as e:
                logger.error(f"Error processing single change {event.file_path}: {e}")
                self.stats["errors_encountered"] += 1
    
    async def _handle_file_content_change(self, event: FileChangeEvent) -> None:
        """Handle file content change (creation or modification)"""
        try:
            file_path = event.file_path
            
            # Read current file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    new_content = f.read()
            except UnicodeDecodeError:
                # Try with different encoding
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    new_content = f.read()
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")
                return
            
            # Get old content from cache
            old_content = self.file_content_cache.get(file_path, "")
            
            # Update cache
            self.file_content_cache[file_path] = new_content
            
            # Skip if content hasn't actually changed
            if old_content == new_content:
                return
            
            # Get content ID for knowledge system
            content_id = self._get_content_id(file_path)
            
            if self.config["auto_trigger_enabled"]:
                # Trigger knowledge evolution
                success = await self.living_knowledge_core.update_content(content_id, new_content)
                
                if success:
                    self.stats["evolutions_triggered"] += 1
                    logger.info(f"Knowledge evolution triggered for: {file_path}")
                
                # Perform semantic analysis if enabled
                if self.config["semantic_analysis_enabled"] and old_content:
                    await self._perform_semantic_analysis(file_path, old_content, new_content)
            
            # Publish file change event
            await self.event_bus.publish(SystemEvent(
                event_type=f"file.{event.change_type.value}",
                entity_id=content_id,
                data={
                    "file_path": file_path,
                    "content_length": len(new_content),
                    "auto_triggered": self.config["auto_trigger_enabled"]
                }
            ))
            
        except Exception as e:
            logger.error(f"Error handling file content change: {e}")
            self.stats["errors_encountered"] += 1
    
    async def _handle_file_deletion(self, event: FileChangeEvent) -> None:
        """Handle file deletion"""
        try:
            file_path = event.file_path
            content_id = self._get_content_id(file_path)
            
            # Remove from cache
            self.file_content_cache.pop(file_path, None)
            
            # Publish deletion event
            await self.event_bus.publish(SystemEvent(
                event_type="file.deleted",
                entity_id=content_id,
                data={"file_path": file_path}
            ))
            
            logger.info(f"File deletion handled: {file_path}")
            
        except Exception as e:
            logger.error(f"Error handling file deletion: {e}")
            self.stats["errors_encountered"] += 1
    
    async def _handle_file_move(self, event: FileChangeEvent) -> None:
        """Handle file move/rename"""
        try:
            old_path = event.old_path
            new_path = event.file_path
            
            # Update cache entry
            if old_path in self.file_content_cache:
                content = self.file_content_cache.pop(old_path)
                self.file_content_cache[new_path] = content
            
            # Publish move event
            await self.event_bus.publish(SystemEvent(
                event_type="file.moved",
                entity_id=self._get_content_id(new_path),
                data={
                    "old_path": old_path,
                    "new_path": new_path
                }
            ))
            
            logger.info(f"File move handled: {old_path} → {new_path}")
            
        except Exception as e:
            logger.error(f"Error handling file move: {e}")
            self.stats["errors_encountered"] += 1
    
    async def _perform_semantic_analysis(self, file_path: str, old_content: str, new_content: str) -> None:
        """Perform semantic analysis on content change"""
        try:
            from trm_api.core.living_knowledge_core import ContentSnapshot, SemanticVersion
            
            # Create snapshots
            old_snapshot = ContentSnapshot(
                content_id=self._get_content_id(file_path),
                content_text=old_content,
                semantic_hash="",
                version=SemanticVersion()
            )
            
            new_snapshot = ContentSnapshot(
                content_id=self._get_content_id(file_path),
                content_text=new_content,
                semantic_hash="",
                version=SemanticVersion()
            )
            
            # Perform semantic analysis
            analysis = await self.semantic_detector.detect_semantic_changes(old_snapshot, new_snapshot)
            
            self.stats["semantic_analyses_performed"] += 1
            
            # Publish semantic analysis results
            await self.event_bus.publish(SystemEvent(
                event_type="semantic.analysis.completed",
                entity_id=analysis.content_id,
                data={
                    "file_path": file_path,
                    "change_type": analysis.detected_change_type,
                    "significance": analysis.overall_significance,
                    "confidence": analysis.confidence_score,
                    "recommended_actions": analysis.recommended_actions
                }
            ))
            
            logger.info(
                f"Semantic analysis completed for {file_path}: "
                f"{analysis.detected_change_type} (significance: {analysis.overall_significance:.2f})"
            )
            
        except Exception as e:
            logger.error(f"Error performing semantic analysis: {e}")
            self.stats["errors_encountered"] += 1
    
    def _get_content_id(self, file_path: str) -> str:
        """Generate content ID from file path"""
        # Convert file path to content ID
        return f"file:{file_path.replace(os.sep, '/')}"
    
    async def add_watched_path(self, watched_path: WatchedPath) -> bool:
        """Add new watched path"""
        try:
            self.watched_paths.append(watched_path)
            
            if self.is_running:
                # Restart watcher với new paths
                await self.watcher.stop_watching()
                await self.watcher.start_watching(self.watched_paths)
            
            logger.info(f"Added watched path: {watched_path.path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding watched path: {e}")
            return False
    
    async def remove_watched_path(self, path: str) -> bool:
        """Remove watched path"""
        try:
            self.watched_paths = [wp for wp in self.watched_paths if wp.path != path]
            
            if self.is_running:
                # Restart watcher với updated paths
                await self.watcher.stop_watching()
                await self.watcher.start_watching(self.watched_paths)
            
            logger.info(f"Removed watched path: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing watched path: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            **self.stats,
            "watched_paths_count": len(self.watched_paths),
            "queue_size": len(self.processing_queue.pending_changes),
            "processing_count": len(self.processing_queue.processing_changes),
            "cache_size": len(self.file_content_cache),
            "is_running": self.is_running
        }
    
    async def stop_monitoring(self) -> None:
        """Stop file system monitoring"""
        try:
            self.is_running = False
            
            if self.processing_task:
                self.processing_task.cancel()
                try:
                    await self.processing_task
                except asyncio.CancelledError:
                    pass
            
            await self.watcher.stop_watching()
            
            # Publish stop event
            await self.event_bus.publish(SystemEvent(
                event_type="agent.data_sensing.stopped",
                entity_id=self.agent_id,
                data=self.get_stats()
            ))
            
            logger.info("DataSensingAgent monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping DataSensingAgent: {e}")


# Global data sensing agent instance
_data_sensing_agent: Optional[DataSensingAgent] = None

async def get_data_sensing_agent() -> DataSensingAgent:
    """Get global data sensing agent instance"""
    global _data_sensing_agent
    if _data_sensing_agent is None:
        _data_sensing_agent = DataSensingAgent()
        await _data_sensing_agent.initialize()
    return _data_sensing_agent 