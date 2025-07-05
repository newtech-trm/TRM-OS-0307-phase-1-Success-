# TRM-OS: Ontology-First Knowledge Management System

[![Tests](https://img.shields.io/badge/tests-220%2F220%20passing-brightgreen)](https://github.com/trm-os/trm-os-branches)
[![API Version](https://img.shields.io/badge/API-v1.0-blue)](https://github.com/trm-os/trm-os-branches)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-orange)](https://neo4j.com)

**TRM-OS** (Total Recall Machine - Operating System) là một hệ thống quản lý tri thức thế hệ mới, vận hành theo nguyên lý **Ontology-First** với kiến trúc **Event-Driven** và **AI Agent Ecosystem**.

## 🎯 Tầm Nhìn

TRM-OS hướng tới việc xây dựng một **"hệ thần kinh trung ương số"** cho tổ chức, một hệ thống thông minh, tự học, tự thích ứng và tự vận hành dựa trên triết lý cốt lõi:

**Recognition → Event → WIN**

- **Recognition (Công nhận)**: Phát hiện và ghi nhận mọi đóng góp, tiềm năng, tension (vấn đề/cơ hội)
- **Event (Sự kiện)**: Ghi lại mọi thay đổi quan trọng trong hệ thống  
- **WIN (Thắng lợi)**: Kết quả tích cực từ việc giải quyết tension hoặc hoàn thành dự án

## 🏗️ Kiến Trúc

### Core Components
- **Graph Database**: Neo4j với 29+ graph models
- **API Layer**: FastAPI với 80+ RESTful endpoints
- **Data Adapters**: Chuẩn hóa DateTime, Enum, và Response data
- **Event System**: Event-driven architecture cho real-time processing
- **Relationship Engine**: Quản lý mối quan hệ phức tạp giữa entities

### Technology Stack
- **Backend**: Python 3.11+ với FastAPI
- **Database**: Neo4j AuraDB (Graph) + PostgreSQL (Vector)
- **Testing**: Pytest với 220+ comprehensive tests
- **Documentation**: OpenAPI/Swagger auto-generated
- **Deployment**: Docker + Docker Compose

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Neo4j AuraDB instance
- Git

### Installation

1. **Clone repository**
```bash
git clone https://github.com/trm-os/trm-os-branches.git
cd trm-os-branches
```

2. **Setup virtual environment**
```bash
# Windows
python -m venv venv-trm
venv-trm\Scripts\activate

# Linux/Mac
python -m venv venv-trm
source venv-trm/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
# Copy và chỉnh sửa environment file
cp .env.example .env
# Cập nhật các biến môi trường trong .env
```

5. **Run application**
```bash
# Development mode
python -m uvicorn trm_api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python -m uvicorn trm_api.main:app --host 0.0.0.0 --port 8000
```

6. **Access API Documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Run All Tests
```bash
# Run all 220 tests
python -m pytest tests/ --tb=short

# Run with coverage
python -m pytest tests/ --cov=trm_api --cov-report=html

# Run specific test categories
python -m pytest tests/unit/ -v          # Unit tests
python -m pytest tests/integration/ -v   # Integration tests  
python -m pytest tests/api/ -v          # API tests
```

### Test Categories
- **Unit Tests**: 150+ tests cho core logic
- **Integration Tests**: 50+ tests cho relationships
- **API Tests**: 20+ tests cho endpoints
- **All Tests**: 220/220 PASSING ✅

## 📚 API Documentation

### Core Entities
- **Agents**: Quản lý con người, AI agents, đối tác
- **Projects**: Theo dõi dự án từ tạo → thực hiện → hoàn thành  
- **Tasks**: Giao việc, theo dõi tiến độ, quản lý assignees
- **WINs**: Ghi nhận thành tựu, đo lường impact
- **Recognitions**: Công nhận đóng góp, kết nối với WINs
- **Knowledge Snippets**: Lưu trữ tri thức, kinh nghiệm
- **Events**: Ghi lại mọi sự kiện quan trọng
- **Tensions**: Quản lý vấn đề và cơ hội

### Key Relationships
- `GIVEN_BY`: Recognition được trao bởi ai
- `RECEIVED_BY`: Recognition được nhận bởi ai
- `RECOGNIZES_WIN`: Recognition công nhận WIN nào  
- `GENERATES_KNOWLEDGE`: WIN tạo ra tri thức gì
- `LEADS_TO_WIN`: Project/Event dẫn đến WIN
- `RESOLVES`: Task giải quyết tension nào

### API Endpoints

#### Entities CRUD
```
GET    /api/v1/{entity}/              # List entities
POST   /api/v1/{entity}/              # Create entity
GET    /api/v1/{entity}/{id}          # Get entity by ID
PUT    /api/v1/{entity}/{id}          # Update entity
DELETE /api/v1/{entity}/{id}          # Delete entity
```

#### Relationships
```
POST   /api/v1/{entity}/{id}/relationships/{relationship_type}/{target_id}
DELETE /api/v1/{entity}/{id}/relationships/{relationship_type}/{target_id}
GET    /api/v1/{entity}/{id}/relationships/{relationship_type}
```

#### Specialized Endpoints
```
GET    /api/v1/recognitions/{id}/wins                    # WINs recognized
GET    /api/v1/wins/{id}/knowledge-snippets              # Knowledge generated
GET    /api/v1/agents/{id}/recognitions/given            # Recognitions given
GET    /api/v1/agents/{id}/recognitions/received         # Recognitions received
```

## 🐳 Docker Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
# Build production image
docker build -t trm-os:latest .

# Run with production config
docker run -d \
  --name trm-os-api \
  -p 8000:8000 \
  --env-file .env \
  trm-os:latest
```

## 🔧 Configuration

### Environment Variables
```bash
# Neo4j Configuration
NEO4J_URI=bolt+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=TRM-OS
VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (optional)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## 📁 Project Structure

```
trm-os-branches/
├── trm_api/                    # Main application code
│   ├── api/v1/                # API endpoints
│   ├── core/                  # Core configuration
│   ├── models/                # Pydantic models
│   ├── graph_models/          # Neo4j graph models
│   ├── services/              # Business logic
│   ├── repositories/          # Data access layer
│   ├── adapters/              # Data transformation
│   └── utils/                 # Utilities
├── tests/                     # Test suite (220 tests)
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── api/                   # API tests
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
├── migrations/                # Database migrations
└── docker-compose.yml         # Docker configuration
```

## 🔄 Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Develop & test
python -m pytest tests/ -x

# Submit PR
git push origin feature/new-feature
```

### 2. Code Quality
```bash
# Format code
black trm_api/
isort trm_api/

# Lint code  
flake8 trm_api/
mypy trm_api/

# Security check
bandit -r trm_api/
```

### 3. Database Migrations
```bash
# Create migration
python scripts/create_migration.py "migration_name"

# Apply migrations
python scripts/apply_migrations.py
```

## 📊 Monitoring & Observability

### Health Checks
```bash
# API Health
curl http://localhost:8000/health

# Database Health
curl http://localhost:8000/health/database
```

### Metrics & Logging
- **Application Logs**: Structured JSON logging
- **Performance Metrics**: Request/response times
- **Error Tracking**: Comprehensive error handling
- **Database Monitoring**: Neo4j query performance

## 🚦 API v2 Roadmap

### Planned Features
- **Real-time WebSocket API**: Live updates cho entities
- **Advanced AI Agents**: Automated decision making
- **GraphQL Support**: Flexible query capabilities  
- **Multi-tenant Architecture**: Support multiple organizations
- **Advanced Analytics**: Business intelligence dashboard
- **External Integrations**: Slack, Teams, Google Workspace

### Migration Path
- **v1 → v2**: Backward compatible migration
- **Deprecation Timeline**: 6 months support for v1
- **Migration Tools**: Automated data migration scripts

## 🤝 Contributing

### Getting Started
1. Fork repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass (220/220)
5. Submit pull request

### Code Standards
- **Test Coverage**: Maintain 95%+ coverage
- **Documentation**: Update API docs for changes
- **Type Hints**: Full type annotation required
- **Error Handling**: Comprehensive error management

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **Architecture**: [docs/architecture/](docs/architecture/)
- **Integration Guide**: [docs/integration-specs/](docs/integration-specs/)

### Community
- **Issues**: [GitHub Issues](https://github.com/trm-os/trm-os-branches/issues)
- **Discussions**: [GitHub Discussions](https://github.com/trm-os/trm-os-branches/discussions)
- **Email**: support@trm-os.com

---

**Built with ❤️ by the TRM Team**

*TRM-OS: Transforming organizations through intelligent knowledge management* 