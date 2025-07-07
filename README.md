# TRM-OS: Ontology-First Knowledge Management System with AI-Enhanced Intelligence

[![Tests](https://img.shields.io/badge/tests-124%2F124%20passing-brightgreen)](https://github.com/trm-os/trm-os-branches)
[![API Version](https://img.shields.io/badge/API-v2.0-blue)](https://github.com/trm-os/trm-os-branches)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)](https://fastapi.tiangolo.com)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-orange)](https://neo4j.com)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.7+-red)](https://scikit-learn.org)

**TRM-OS** (Total Recall Machine - Operating System) là một hệ thống quản lý tri thức thế hệ mới với **AI-Enhanced Intelligence** và **Conversational Intelligence**, vận hành theo nguyên lý **Ontology-First** với kiến trúc **Event-Driven** và **ML-Enhanced Reasoning**.

## 🎯 Tầm Nhìn

TRM-OS hướng tới việc xây dựng một **"hệ thần kinh trung ương số"** cho tổ chức, một hệ thống thông minh, tự học, tự thích ứng và tự vận hành dựa trên triết lý cốt lõi:

**Recognition → Event → WIN**

- **Recognition (Công nhận)**: Phát hiện và ghi nhận mọi đóng góp, tiềm năng, tension (vấn đề/cơ hội)
- **Event (Sự kiện)**: Ghi lại mọi thay đổi quan trọng trong hệ thống  
- **WIN (Thắng lợi)**: Kết quả tích cực từ việc giải quyết tension hoặc hoàn thành dự án

## 🧠 AI-Enhanced Intelligence

### 💬 Conversational Intelligence (NEW!)
- **Natural Language Processing**: Vietnamese và English support với 95%+ accuracy
- **Intent Recognition**: 10 intent types với intelligent reasoning type mapping
- **ML-Enhanced Conversations**: Real-time ML reasoning integration cho intelligent responses
- **Session Management**: Advanced conversation context tracking và memory
- **Real-time Communication**: WebSocket support cho instant messaging
- **Multi-language Support**: Seamless Vietnamese/English conversation switching
- **Context-Aware Responses**: Learning-based response adaptation

### ML-Enhanced Reasoning Engine
- **Multi-Type Reasoning**: Deductive, Inductive, Abductive, Analogical, Causal, Probabilistic, Quantum, Hybrid
- **Real ML Models**: RandomForest, GradientBoosting, KMeans cho reasoning type prediction và confidence estimation
- **Quantum Enhancement**: Tích hợp với Quantum WIN States cho advanced reasoning
- **Context-Aware**: Reasoning recommendations dựa trên context và historical patterns
- **Performance Analytics**: Real-time reasoning statistics và pattern discovery

### Adaptive Learning System
- **Experience Collection**: Thu thập và phân tích 24+ loại experience types
- **Pattern Recognition**: Tự động phát hiện patterns từ agent behaviors và outcomes
- **Behavioral Adaptation**: Tự động điều chỉnh strategies dựa trên learning outcomes
- **Goal Management**: Tracking và optimization learning goals
- **Performance Metrics**: Comprehensive metrics cho learning effectiveness

### Quantum System Manager
- **Quantum State Detection**: ML-powered detection của organizational quantum states
- **WIN Probability Calculation**: Quantum-enhanced probability calculations
- **State Transition Optimization**: Intelligent state transition recommendations
- **Coherence Monitoring**: Real-time quantum coherence tracking

## 🏗️ Kiến Trúc

### Core Components
- **Graph Database**: Neo4j với 29+ graph models
- **API Layer**: FastAPI với 80+ RESTful endpoints + ML reasoning endpoints + Conversational endpoints
- **Conversational Intelligence**: Multi-language NLP với ML-enhanced reasoning
- **ML-Enhanced Reasoning**: Production-ready reasoning engine với real ML models
- **Adaptive Learning**: Self-improving system với experience-based learning
- **Quantum Intelligence**: Quantum-enhanced decision making và optimization
- **Event System**: Event-driven architecture cho real-time processing
- **Relationship Engine**: Quản lý mối quan hệ phức tạp giữa entities

### Technology Stack
- **Backend**: Python 3.11+ với FastAPI
- **Machine Learning**: Scikit-learn 1.7+ với RandomForest, GradientBoosting, KMeans
- **NLP**: Advanced Vietnamese/English natural language processing
- **Real-time**: WebSocket support cho instant communication
- **Database**: Neo4j AuraDB (Graph) + PostgreSQL (Vector)
- **Testing**: Pytest với 124+ comprehensive tests
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
# Run all 124 tests
python -m pytest tests/unit/ --tb=short

# Run with coverage
python -m pytest tests/unit/ --cov=trm_api --cov-report=html

# Test ML-Enhanced Reasoning Engine
python test_ml_reasoning_simple.py

# Test specific components
python -m pytest tests/unit/test_adaptive_learning_system.py -v
python -m pytest tests/unit/test_advanced_reasoning_engine.py -v
```

### Test Categories
- **Unit Tests**: 124+ tests cho core logic
- **ML Reasoning Tests**: Comprehensive tests cho ML-enhanced reasoning
- **Adaptive Learning Tests**: 17+ tests cho adaptive learning system
- **All Tests**: 124/124 PASSING ✅

## 🤖 ML-Enhanced API Documentation

### ML Reasoning Endpoints
```
POST   /api/v1/ml-reasoning/reason              # Perform ML-enhanced reasoning
POST   /api/v1/ml-reasoning/train               # Train ML models
GET    /api/v1/ml-reasoning/patterns            # Analyze reasoning patterns
POST   /api/v1/ml-reasoning/recommendations     # Get reasoning recommendations
GET    /api/v1/ml-reasoning/statistics          # Get performance metrics
GET    /api/v1/ml-reasoning/health              # Health check
```

### Reasoning Types Supported
- **Deductive**: Logic-based reasoning từ general principles
- **Inductive**: Pattern-based reasoning từ specific observations
- **Abductive**: Best-explanation reasoning cho incomplete information
- **Analogical**: Similarity-based reasoning using analogies
- **Causal**: Cause-effect relationship reasoning
- **Probabilistic**: Statistical và probability-based reasoning
- **Quantum**: Quantum-enhanced reasoning với WIN probability
- **Hybrid**: Combination của multiple reasoning types

### ML Models Used
- **RandomForestClassifier**: Reasoning type prediction
- **GradientBoostingRegressor**: Confidence estimation
- **KMeans**: Context clustering và pattern recognition

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
VERSION=2.0.0

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Configuration
ML_MODEL_PATH=./models/
REASONING_CONFIDENCE_THRESHOLD=0.7
LEARNING_RATE=0.001

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
├── tests/                     # Test suite (124 tests)
│   ├── unit/                  # Unit tests
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
4. Ensure all tests pass (124/124)
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

## 💬 Conversational Intelligence API

### Conversation Endpoints
```
POST   /api/v2/conversations/analyze            # Analyze natural language message
POST   /api/v2/conversations/sessions           # Create conversation session
GET    /api/v2/conversations/sessions/{id}      # Get session info
DELETE /api/v2/conversations/sessions/{id}      # End session
GET    /api/v2/conversations/sessions/{id}/history     # Get conversation history
GET    /api/v2/conversations/sessions/{id}/analytics   # Get session analytics
WS     /api/v2/conversations/realtime/{id}      # Real-time WebSocket chat
GET    /api/v2/conversations/health             # Health check
```

### Supported Intents
- **CREATE_PROJECT**: Tạo dự án mới
- **ANALYZE_TENSION**: Phân tích vấn đề/cơ hội
- **GET_AGENT_HELP**: Tìm kiếm trợ giúp từ agents
- **CHECK_STATUS**: Kiểm tra trạng thái công việc
- **GENERATE_SOLUTION**: Tạo giải pháp cho vấn đề
- **SEARCH_KNOWLEDGE**: Tìm kiếm thông tin/tri thức
- **UPDATE_RESOURCE**: Cập nhật tài nguyên
- **SCHEDULE_TASK**: Lên lịch công việc
- **GET_INSIGHTS**: Lấy insights và phân tích

### Example Conversation Flow
```python
# 1. Create conversation session
session = await conversation_manager.create_session(user_id="user123")

# 2. Send message
response = await conversation_manager.analyze(
    session_id=session.session_id,
    message="Tôi cần tạo dự án AI mới với team 5 người",
    language="vi"
)

# 3. Get ML-enhanced response
print(f"Intent: {response.intent_detected}")
print(f"Confidence: {response.confidence}")
print(f"Response: {response.response_text}")
print(f"Actions: {response.suggested_actions}")
``` 