# 📐 TRM-OS PROJECT STANDARDIZATION GUIDE
## Hướng Dẫn Chuẩn Hóa Dự Án Hoàn Chỉnh

### 🎯 **MỤC TIÊU CHUẨN HÓA**

1. **Code Consistency**: Uniform coding standards across all modules
2. **Architecture Alignment**: Consistent patterns và structures
3. **Documentation Standards**: Complete và up-to-date documentation
4. **Testing Standards**: Comprehensive test coverage
5. **Deployment Standards**: Reliable và repeatable deployments

### 📁 **CHUẨN HÓA CẤU TRÚC DỰ ÁN**

#### **Current Structure (Standardized)**
```
trm-os-branches/
├── 📁 trm_api/                 # Core application
│   ├── 📁 api/v1/              # API version 1
│   │   ├── 📁 endpoints/       # REST endpoints
│   │   ├── 📁 models/          # Request/Response models  
│   │   └── 📄 api.py           # Router aggregation
│   ├── 📁 models/              # Pydantic data models
│   ├── 📁 graph_models/        # Neo4j OGM models
│   ├── 📁 repositories/        # Data access layer
│   ├── 📁 services/            # Business logic layer
│   ├── 📁 adapters/            # Data transformation
│   ├── 📁 middleware/          # Request/Response middleware
│   ├── 📁 core/                # Configuration & utilities
│   ├── 📁 db/                  # Database connections
│   ├── 📁 eventbus/            # Event handling
│   ├── 📁 schemas/             # Data schemas
│   ├── 📁 utils/               # Utility functions
│   └── 📄 main.py              # Application entry point
├── 📁 tests/                   # Test suite
│   ├── 📁 api/                 # API endpoint tests
│   ├── 📁 integration/         # Integration tests
│   ├── 📁 unit/                # Unit tests
│   └── 📄 conftest.py          # Test configuration
├── 📁 docs/                    # Documentation
│   ├── 📁 architecture/        # System architecture docs
│   ├── 📁 core-specs/          # Core specifications
│   ├── 📁 integration-specs/   # Integration patterns
│   ├── 📁 technical-decisions/ # Technical decisions
│   └── 📄 *.md                 # Various documentation
├── 📁 scripts/                 # Utility scripts
├── 📁 migrations/              # Database migrations
├── 📁 tools/                   # Development tools
├── 📄 requirements.txt         # Python dependencies
├── 📄 Dockerfile              # Container configuration
├── 📄 docker-compose.yml      # Local development
├── 📄 pytest.ini              # Test configuration
└── 📄 README.md                # Project overview
```

### 🏗️ **ARCHITECTURE PATTERNS**

#### **1. Layered Architecture**
```
┌─────────────────────────────────────┐
│           API Layer                 │  ← REST endpoints
├─────────────────────────────────────┤
│         Service Layer               │  ← Business logic
├─────────────────────────────────────┤
│       Repository Layer              │  ← Data access
├─────────────────────────────────────┤
│         Model Layer                 │  ← Data models
└─────────────────────────────────────┘
```

#### **2. Adapter Pattern**
```python
# Standard adapter structure
class EntityAdapter(BaseEntityAdapter):
    def __init__(self, adapt_datetime=True, adapt_enums=True):
        super().__init__(adapt_datetime, adapt_enums)
    
    def apply_to_entity(self, data: dict) -> dict:
        # Entity-specific transformations
        return super().apply_to_entity(data)
```

#### **3. Repository Pattern**
```python
# Standard repository structure
class EntityRepository:
    async def create_entity(self, entity_data: EntityCreate) -> Entity:
        pass
    
    async def get_entity_by_uid(self, uid: str) -> Optional[Entity]:
        pass
    
    async def list_entities(self, skip: int = 0, limit: int = 100) -> List[Entity]:
        pass
    
    async def update_entity(self, uid: str, entity_data: EntityUpdate) -> Optional[Entity]:
        pass
    
    async def delete_entity(self, uid: str) -> bool:
        pass
```

### 📋 **NAMING CONVENTIONS**

#### **1. File Naming**
- **Python files**: `snake_case.py`
- **Test files**: `test_module_name.py`
- **Documentation**: `UPPER_CASE.md` hoặc `Title_Case.md`

#### **2. Class Naming**
```python
# Models
class Agent(BaseModel): pass           # Entity models
class AgentCreate(BaseModel): pass     # Create models
class AgentUpdate(BaseModel): pass     # Update models
class AgentInDB(BaseModel): pass       # Database models

# Services
class AgentService: pass               # Business logic

# Repositories
class AgentRepository: pass            # Data access

# Adapters
class AgentAdapter(BaseEntityAdapter): pass  # Data transformation
```

#### **3. API Naming**
- **Endpoints**: `/api/v1/entities/` (plural, lowercase)
- **Fields**: `camelCase` trong API responses
- **Parameters**: `snake_case` trong Python code

#### **4. Database Naming**
- **Neo4j Labels**: `PascalCase` (Agent, WIN, Recognition)
- **Properties**: `snake_case` (created_at, agent_type)
- **Relationships**: `UPPER_CASE` (GIVEN_BY, RECEIVED_BY)

### 🎨 **CODE STYLE STANDARDS**

#### **1. Python Code Style**
```python
# Imports order
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException

# Function definitions
async def create_entity(
    entity_data: EntityCreate,
    repo: EntityRepository = Depends(get_repository)
) -> Entity:
    """
    Create a new entity.
    
    Args:
        entity_data: Entity creation data
        repo: Repository dependency
        
    Returns:
        Created entity
        
    Raises:
        HTTPException: If creation fails
    """
    return await repo.create_entity(entity_data)
```

#### **2. Model Definitions**
```python
class EntityBase(BaseModel):
    name: str = Field(..., description="Entity name")
    description: Optional[str] = Field(None, description="Entity description")
    status: str = Field("active", description="Entity status")
    
    @field_validator('field_name', mode='before')
    @classmethod
    def validate_field(cls, v):
        """Convert None to appropriate default"""
        if v is None:
            return default_value
        return v
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Example Entity",
                "description": "Example description",
                "status": "active"
            }
        }
    )
```

### 🧪 **TESTING STANDARDS**

#### **1. Test File Structure**
```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

class TestEntityEndpoints:
    """Test suite for Entity API endpoints"""
    
    def test_create_entity_success(self, test_client):
        """Test successful entity creation"""
        pass
    
    def test_create_entity_validation_error(self, test_client):
        """Test validation error handling"""
        pass
    
    def test_get_entity_success(self, test_client):
        """Test successful entity retrieval"""
        pass
    
    def test_get_entity_not_found(self, test_client):
        """Test 404 for non-existent entity"""
        pass
    
    def test_list_entities_success(self, test_client):
        """Test entity listing"""
        pass
    
    def test_update_entity_success(self, test_client):
        """Test successful entity update"""
        pass
    
    def test_delete_entity_success(self, test_client):
        """Test successful entity deletion"""
        pass
```

#### **2. Test Coverage Requirements**
- **Minimum 80%** overall coverage
- **100%** coverage cho critical paths
- **All endpoints** must have tests
- **Error scenarios** must be tested

### 📚 **DOCUMENTATION STANDARDS**

#### **1. API Documentation**
```python
@router.post("/", response_model=Entity, status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity_in: EntityCreate,
    repo: EntityRepository = Depends(get_repository)
):
    """
    Create a new Entity.
    
    - **name**: Entity name (required)
    - **description**: Entity description (optional)
    - **status**: Entity status (default: active)
    
    Returns the created entity with generated ID and timestamps.
    """
    return await repo.create_entity(entity_data=entity_in)
```

#### **2. README Structure**
```markdown
# Entity Name

## Overview
Brief description of the entity/module.

## Features
- Feature 1
- Feature 2

## Usage
Code examples and usage instructions.

## API Endpoints
List of available endpoints.

## Models
Data model descriptions.

## Testing
How to run tests.
```

### 🔄 **DEVELOPMENT WORKFLOW**

#### **1. Feature Development**
```bash
# 1. Create feature branch
git checkout -b feature/entity-management

# 2. Develop with TDD
# - Write tests first
# - Implement functionality
# - Ensure tests pass

# 3. Code quality checks
pytest tests/ -v --cov=trm_api
black trm_api/
isort trm_api/

# 4. Commit changes
git add .
git commit -m "feat: add entity management endpoints"

# 5. Push and create PR
git push origin feature/entity-management
```

#### **2. Code Review Checklist**
- [ ] Tests written và passing
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance considerations
- [ ] Security considerations

#### **3. Deployment Process**
```bash
# 1. Merge to main branch
git checkout 95-percent
git merge feature/entity-management

# 2. Run full test suite
pytest tests/ -v

# 3. Deploy to production
git push origin 95-percent  # Auto-deploy via Railway

# 4. Verify deployment
curl https://trmosngonlanh.up.railway.app/health
```

### 🛠️ **TOOLS & UTILITIES**

#### **1. Development Tools**
```bash
# Code formatting
black trm_api/
isort trm_api/

# Type checking
mypy trm_api/

# Testing
pytest tests/ -v --cov=trm_api

# Linting
flake8 trm_api/
```

#### **2. Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

### 📊 **QUALITY METRICS**

#### **1. Code Quality**
- **Test Coverage**: >90%
- **Code Complexity**: <10 cyclomatic complexity
- **Documentation**: All public APIs documented
- **Type Hints**: 100% type coverage

#### **2. Performance**
- **API Response Time**: <200ms average
- **Database Queries**: <50ms average
- **Memory Usage**: <512MB per instance
- **CPU Usage**: <70% average

#### **3. Reliability**
- **Uptime**: >99.9%
- **Error Rate**: <0.1%
- **Recovery Time**: <5 minutes
- **Data Consistency**: 100%

### 🔒 **SECURITY STANDARDS**

#### **1. Input Validation**
```python
# Always validate inputs
class EntityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

#### **2. Error Handling**
```python
# Don't expose internal errors
try:
    result = await repo.create_entity(entity_data)
    return result
except ValidationError as e:
    raise HTTPException(status_code=400, detail="Invalid input data")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### 🚀 **DEPLOYMENT STANDARDS**

#### **1. Environment Configuration**
```python
# trm_api/core/config.py
class Settings(BaseSettings):
    neo4j_uri: str = Field(..., env="NEO4J_URI")
    neo4j_user: str = Field(..., env="NEO4J_USER")
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")
    
    class Config:
        env_file = ".env"
```

#### **2. Health Checks**
```python
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

#### **3. Monitoring**
```python
# Add logging to all critical functions
import logging

logger = logging.getLogger(__name__)

async def create_entity(entity_data: EntityCreate):
    logger.info(f"Creating entity: {entity_data.name}")
    try:
        result = await repo.create_entity(entity_data)
        logger.info(f"Entity created successfully: {result.uid}")
        return result
    except Exception as e:
        logger.error(f"Failed to create entity: {e}")
        raise
```

### 📈 **CONTINUOUS IMPROVEMENT**

#### **1. Regular Reviews**
- **Weekly**: Code review sessions
- **Monthly**: Architecture review
- **Quarterly**: Performance analysis
- **Annually**: Technology stack review

#### **2. Metrics Tracking**
- **Development velocity**
- **Bug resolution time**
- **Test coverage trends**
- **Performance metrics**

#### **3. Knowledge Sharing**
- **Documentation updates**
- **Best practices sharing**
- **Technical decision records**
- **Lessons learned sessions**

---

## 🎯 **IMMEDIATE ACTION ITEMS**

### **Priority 1: Critical**
1. **Complete test coverage** cho tất cả endpoints
2. **Standardize field validators** cho all models
3. **Implement missing adapters**
4. **Update documentation**

### **Priority 2: Important**
1. **Add authentication layer**
2. **Performance optimization**
3. **Error handling standardization**
4. **Monitoring implementation**

### **Priority 3: Enhancement**
1. **Code quality tools setup**
2. **CI/CD pipeline improvement**
3. **Advanced features planning**
4. **Integration testing expansion**

**🎯 Goal: Achieve "HOÀN TOÀN NGON LÀNH" standard across all aspects of the project!** 