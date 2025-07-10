"""
Output Normalization Schema System

Enterprise-grade output normalization, validation, and standardization
for consistent API responses across all TRM-OS components.
"""

from typing import Dict, Any, List, Optional, Union, Type, Generic, TypeVar, get_args, get_origin
import json
import math
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
import jsonschema
from jsonschema import validate, ValidationError
from pydantic import BaseModel, Field, validator, ValidationError as PydanticValidationError
import uuid
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ResponseStatus(str, Enum):
    """Standard response status codes"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    PENDING = "pending"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    TIMEOUT = "timeout"


class DataFormat(str, Enum):
    """Supported data formats"""
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    YAML = "yaml"
    PROTOBUF = "protobuf"


class NormalizationLevel(str, Enum):
    """Normalization strictness levels"""
    STRICT = "strict"      # Reject any non-conforming data
    PERMISSIVE = "permissive"  # Try to convert/fix data
    LOOSE = "loose"        # Allow most data through with warnings


@dataclass
class ValidationResult:
    """Result of data validation"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    normalized_data: Optional[Any] = None
    schema_version: str = "1.0"


@dataclass
class MetaData:
    """Response metadata"""
    request_id: str
    timestamp: datetime
    processing_time_ms: float
    api_version: str = "1.0"
    schema_version: str = "1.0"
    source: str = "trm-os"
    total_count: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    has_more: bool = False


class StandardResponse(BaseModel, Generic[T]):
    """
    Standard normalized response format for all TRM-OS APIs
    
    Ensures consistent structure across all responses
    """
    status: ResponseStatus
    data: Optional[T] = None
    message: str = ""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: MetaData
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
            uuid.UUID: lambda v: str(v)
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response format"""
    status: ResponseStatus
    data: List[T] = Field(default_factory=list)
    message: str = ""
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: MetaData
    pagination: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True


class ErrorDetail(BaseModel):
    """Detailed error information"""
    code: str
    message: str
    field: Optional[str] = None
    value: Optional[Any] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class SchemaDefinition(BaseModel):
    """Schema definition for data validation"""
    name: str
    version: str
    description: str
    schema: Dict[str, Any]
    examples: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class OutputNormalizer:
    """
    Enterprise Output Normalizer
    
    Features:
    - Schema-based validation and normalization
    - Multiple data format support
    - Configurable strictness levels
    - Custom validation rules
    - Performance monitoring
    - Error aggregation and reporting
    """
    
    def __init__(
        self,
        default_level: NormalizationLevel = NormalizationLevel.PERMISSIVE,
        enable_caching: bool = True,
        cache_size: int = 1000
    ):
        self.default_level = default_level
        self.enable_caching = enable_caching
        self.cache_size = cache_size
        
        # Schema registry
        self._schemas: Dict[str, SchemaDefinition] = {}
        self._custom_validators: Dict[str, callable] = {}
        
        # Performance tracking
        self._validation_count = 0
        self._error_count = 0
        self._cache_hits = 0
        self._cache_misses = 0
        
        # Validation cache
        self._validation_cache: Dict[str, ValidationResult] = {}
        
        # Register built-in schemas
        self._register_builtin_schemas()
        
        logger.info("Output Normalizer initialized")
    
    # ================================
    # SCHEMA MANAGEMENT
    # ================================
    
    def register_schema(
        self,
        name: str,
        schema: Dict[str, Any],
        version: str = "1.0",
        description: str = "",
        examples: Optional[List[Dict[str, Any]]] = None
    ):
        """Register new schema for validation"""
        schema_def = SchemaDefinition(
            name=name,
            version=version,
            description=description,
            schema=schema,
            examples=examples or []
        )
        
        self._schemas[name] = schema_def
        logger.info(f"Registered schema: {name} v{version}")
    
    def get_schema(self, name: str) -> Optional[SchemaDefinition]:
        """Get schema definition by name"""
        return self._schemas.get(name)
    
    def list_schemas(self) -> List[str]:
        """List all registered schema names"""
        return list(self._schemas.keys())
    
    def register_custom_validator(self, name: str, validator_func: callable):
        """Register custom validation function"""
        self._custom_validators[name] = validator_func
        logger.info(f"Registered custom validator: {name}")
    
    # ================================
    # NORMALIZATION AND VALIDATION
    # ================================
    
    def normalize(
        self,
        data: Any,
        schema_name: Optional[str] = None,
        level: Optional[NormalizationLevel] = None,
        format_type: DataFormat = DataFormat.JSON
    ) -> ValidationResult:
        """
        Normalize and validate data according to schema
        
        Args:
            data: Data to normalize
            schema_name: Schema to validate against
            level: Normalization strictness level
            format_type: Expected data format
            
        Returns:
            ValidationResult with normalized data or errors
        """
        level = level or self.default_level
        
        # Generate cache key
        cache_key = self._generate_cache_key(data, schema_name, level, format_type)
        
        # Check cache
        if self.enable_caching and cache_key in self._validation_cache:
            self._cache_hits += 1
            return self._validation_cache[cache_key]
        
        self._cache_misses += 1
        self._validation_count += 1
        
        try:
            # Step 1: Format conversion if needed
            if format_type != DataFormat.JSON:
                data = self._convert_format(data, format_type, DataFormat.JSON)
            
            # Step 2: Basic data cleaning and normalization
            normalized_data = self._normalize_data(data, level)
            
            # Step 3: Schema validation if specified
            validation_errors = []
            if schema_name:
                validation_errors = self._validate_against_schema(normalized_data, schema_name)
            
            # Step 4: Custom validation
            custom_errors = self._run_custom_validations(normalized_data, schema_name)
            validation_errors.extend(custom_errors)
            
            # Step 5: Create result
            is_valid = len(validation_errors) == 0
            if not is_valid:
                self._error_count += 1
            
            result = ValidationResult(
                is_valid=is_valid,
                errors=validation_errors,
                normalized_data=normalized_data if is_valid or level != NormalizationLevel.STRICT else None
            )
            
            # Cache result
            if self.enable_caching:
                self._cache_result(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Normalization failed: {str(e)}")
            self._error_count += 1
            
            return ValidationResult(
                is_valid=False,
                errors=[f"Normalization error: {str(e)}"]
            )
    
    def create_standard_response(
        self,
        data: Any = None,
        status: ResponseStatus = ResponseStatus.SUCCESS,
        message: str = "",
        request_id: Optional[str] = None,
        processing_time_ms: Optional[float] = None,
        errors: Optional[List[Dict[str, Any]]] = None,
        warnings: Optional[List[str]] = None,
        **metadata_kwargs
    ) -> StandardResponse:
        """Create standardized response object"""
        
        # Generate request ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Create metadata
        metadata = MetaData(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time_ms or 0.0,
            **metadata_kwargs
        )
        
        return StandardResponse(
            status=status,
            data=data,
            message=message,
            errors=errors or [],
            warnings=warnings or [],
            metadata=metadata
        )
    
    def create_paginated_response(
        self,
        data: List[Any],
        total_count: int,
        page: int = 1,
        page_size: int = 20,
        status: ResponseStatus = ResponseStatus.SUCCESS,
        message: str = "",
        request_id: Optional[str] = None,
        processing_time_ms: Optional[float] = None,
        **kwargs
    ) -> PaginatedResponse:
        """Create standardized paginated response"""
        
        # Generate request ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Calculate pagination info
        has_more = (page * page_size) < total_count
        total_pages = (total_count + page_size - 1) // page_size
        
        # Create metadata
        metadata = MetaData(
            request_id=request_id,
            timestamp=datetime.now(),
            processing_time_ms=processing_time_ms or 0.0,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_more=has_more
        )
        
        # Create pagination details
        pagination = {
            'current_page': page,
            'page_size': page_size,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_previous': page > 1,
            'has_next': has_more,
            'previous_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if has_more else None
        }
        
        return PaginatedResponse(
            status=status,
            data=data,
            message=message,
            metadata=metadata,
            pagination=pagination,
            **kwargs
        )
    
    def create_error_response(
        self,
        errors: List[Union[str, Dict[str, Any], ErrorDetail]],
        status: ResponseStatus = ResponseStatus.ERROR,
        message: str = "An error occurred",
        request_id: Optional[str] = None,
        **kwargs
    ) -> StandardResponse:
        """Create standardized error response"""
        
        # Normalize errors to consistent format
        normalized_errors = []
        for error in errors:
            if isinstance(error, str):
                normalized_errors.append({
                    'code': 'GENERAL_ERROR',
                    'message': error
                })
            elif isinstance(error, ErrorDetail):
                normalized_errors.append(error.dict())
            elif isinstance(error, dict):
                normalized_errors.append(error)
        
        return self.create_standard_response(
            data=None,
            status=status,
            message=message,
            request_id=request_id,
            errors=normalized_errors,
            **kwargs
        )
    
    # ================================
    # DATA NORMALIZATION
    # ================================
    
    def _normalize_data(self, data: Any, level: NormalizationLevel) -> Any:
        """Normalize data structure and types"""
        if data is None:
            return None
        
        if isinstance(data, dict):
            return self._normalize_dict(data, level)
        elif isinstance(data, list):
            return [self._normalize_data(item, level) for item in data]
        elif isinstance(data, str):
            return self._normalize_string(data, level)
        elif isinstance(data, (int, float)):
            return self._normalize_number(data, level)
        elif isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, date):
            return data.isoformat()
        elif isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, uuid.UUID):
            return str(data)
        else:
            # For other types, convert to string in permissive mode
            if level == NormalizationLevel.STRICT:
                raise ValueError(f"Unsupported data type: {type(data)}")
            return str(data)
    
    def _normalize_dict(self, data: Dict[str, Any], level: NormalizationLevel) -> Dict[str, Any]:
        """Normalize dictionary data"""
        normalized = {}
        
        for key, value in data.items():
            # Normalize key
            normalized_key = self._normalize_string(key, level)
            
            # Normalize value
            normalized_value = self._normalize_data(value, level)
            
            normalized[normalized_key] = normalized_value
        
        return normalized
    
    def _normalize_string(self, data: str, level: NormalizationLevel) -> str:
        """Normalize string data"""
        if level == NormalizationLevel.STRICT:
            return data
        
        # Basic string normalization
        normalized = data.strip()
        
        if level == NormalizationLevel.PERMISSIVE:
            # Remove extra whitespace
            normalized = ' '.join(normalized.split())
        
        return normalized
    
    def _normalize_number(self, data: Union[int, float], level: NormalizationLevel) -> Union[int, float]:
        """Normalize numeric data"""
        # Handle infinity and NaN
        if isinstance(data, float):
            if not math.isfinite(data):
                if level == NormalizationLevel.STRICT:
                    raise ValueError(f"Invalid number: {data}")
                return None
        
        return data
    
    # ================================
    # VALIDATION
    # ================================
    
    def _validate_against_schema(self, data: Any, schema_name: str) -> List[str]:
        """Validate data against registered schema"""
        schema_def = self._schemas.get(schema_name)
        if not schema_def:
            return [f"Schema not found: {schema_name}"]
        
        try:
            validate(instance=data, schema=schema_def.schema)
            return []
        except ValidationError as e:
            return [f"Schema validation error: {e.message}"]
        except Exception as e:
            return [f"Validation error: {str(e)}"]
    
    def _run_custom_validations(self, data: Any, schema_name: Optional[str]) -> List[str]:
        """Run custom validation functions"""
        errors = []
        
        # Run general custom validators
        for name, validator in self._custom_validators.items():
            try:
                if not validator(data):
                    errors.append(f"Custom validation failed: {name}")
            except Exception as e:
                errors.append(f"Custom validator error ({name}): {str(e)}")
        
        return errors
    
    # ================================
    # FORMAT CONVERSION
    # ================================
    
    def _convert_format(self, data: Any, from_format: DataFormat, to_format: DataFormat) -> Any:
        """Convert data between formats"""
        if from_format == to_format:
            return data
        
        # For now, only handle basic conversions
        if from_format == DataFormat.JSON and to_format == DataFormat.JSON:
            return data
        
        # Add more format conversions as needed
        raise NotImplementedError(f"Format conversion from {from_format} to {to_format} not implemented")
    
    # ================================
    # CACHING
    # ================================
    
    def _generate_cache_key(
        self,
        data: Any,
        schema_name: Optional[str],
        level: NormalizationLevel,
        format_type: DataFormat
    ) -> str:
        """Generate cache key for validation result"""
        import hashlib
        
        key_data = {
            'data_hash': hashlib.md5(str(data).encode()).hexdigest(),
            'schema_name': schema_name,
            'level': level.value,
            'format_type': format_type.value
        }
        
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
    
    def _cache_result(self, cache_key: str, result: ValidationResult):
        """Cache validation result with size management"""
        if len(self._validation_cache) >= self.cache_size:
            # Remove oldest entries (simple FIFO)
            keys_to_remove = list(self._validation_cache.keys())[:self.cache_size // 10]
            for key in keys_to_remove:
                del self._validation_cache[key]
        
        self._validation_cache[cache_key] = result
    
    # ================================
    # BUILT-IN SCHEMAS
    # ================================
    
    def _register_builtin_schemas(self):
        """Register built-in validation schemas"""
        
        # Standard API response schema
        response_schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": [s.value for s in ResponseStatus]},
                "data": {},  # Any type allowed for data
                "message": {"type": "string"},
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"},
                            "message": {"type": "string"},
                            "field": {"type": "string"},
                            "value": {}
                        },
                        "required": ["code", "message"]
                    }
                },
                "warnings": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "request_id": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "processing_time_ms": {"type": "number"},
                        "api_version": {"type": "string"},
                        "schema_version": {"type": "string"}
                    },
                    "required": ["request_id", "timestamp", "processing_time_ms"]
                }
            },
            "required": ["status", "metadata"]
        }
        
        self.register_schema(
            "standard_response",
            response_schema,
            description="Standard API response format"
        )
        
        # Entity schemas
        user_schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "role": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            },
            "required": ["uid", "name", "email"]
        }
        
        self.register_schema(
            "user",
            user_schema,
            description="User entity schema"
        )
        
        # Add more built-in schemas as needed
        logger.info("Built-in schemas registered")
    
    # ================================
    # MONITORING AND METRICS
    # ================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get normalization performance statistics"""
        total_validations = self._validation_count
        error_rate = (self._error_count / total_validations * 100) if total_validations > 0 else 0
        cache_hit_rate = (self._cache_hits / (self._cache_hits + self._cache_misses) * 100) if (self._cache_hits + self._cache_misses) > 0 else 0
        
        return {
            'total_validations': total_validations,
            'error_count': self._error_count,
            'error_rate_percent': round(error_rate, 2),
            'cache_hit_rate_percent': round(cache_hit_rate, 2),
            'registered_schemas': len(self._schemas),
            'custom_validators': len(self._custom_validators),
            'cache_size': len(self._validation_cache)
        }
    
    def clear_cache(self):
        """Clear validation cache"""
        self._validation_cache.clear()
        logger.info("Validation cache cleared")


# Global instance
output_normalizer = OutputNormalizer()


# Convenience functions
def normalize_response(
    data: Any = None,
    status: ResponseStatus = ResponseStatus.SUCCESS,
    message: str = "",
    **kwargs
) -> StandardResponse:
    """Create normalized standard response"""
    return output_normalizer.create_standard_response(
        data=data,
        status=status,
        message=message,
        **kwargs
    )


def normalize_error(
    errors: List[Union[str, Dict[str, Any]]],
    message: str = "An error occurred",
    **kwargs
) -> StandardResponse:
    """Create normalized error response"""
    return output_normalizer.create_error_response(
        errors=errors,
        message=message,
        **kwargs
    )


def normalize_data(
    data: Any,
    schema_name: Optional[str] = None,
    **kwargs
) -> ValidationResult:
    """Normalize and validate data"""
    return output_normalizer.normalize(
        data=data,
        schema_name=schema_name,
        **kwargs
    ) 