# TRM-OS API v1.0 - Comprehensive Documentation

*Version: 1.0 | Last Updated: 2025-01-11 | Status: Production Ready*

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)  
3. [Core Entities](#core-entities)
4. [Relationships](#relationships)
5. [API Endpoints](#api-endpoints)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Examples](#examples)
10. [Migration to v2](#migration-to-v2)

---

## 🎯 Overview

TRM-OS API v1.0 là một RESTful API được xây dựng theo nguyên lý **Ontology-First** với kiến trúc **Event-Driven**. API cung cấp khả năng quản lý toàn diện các thực thể và mối quan hệ trong hệ thống quản lý tri thức.

### Base URL
```
Production:  https://api.trm-os.com/api/v1
Development: http://localhost:8000/api/v1
```

### Content Type
```
Content-Type: application/json
Accept: application/json
```

### API Philosophy
API được thiết kế theo triết lý **"Recognition → Event → WIN"**:
- Mọi hành động đều tạo ra Events
- Recognition là điểm khởi đầu của mọi quy trình
- WIN là mục tiêu cuối cùng của mọi hoạt động

---

## 🔐 Authentication

### API Key Authentication
```http
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0 (Coming in v2)
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Service Account
```http
X-Service-Account: service_account_id
Authorization: Bearer SERVICE_ACCOUNT_TOKEN
```

---

## 🏗️ Core Entities

### 1. Agent
**Mô tả**: Đại diện cho các tác nhân hành động (con người, AI, tổ chức)

**Subtypes**:
- `InternalAgent`: Thành viên nội bộ TRM
- `ExternalAgent`: Đối tác, khách hàng, nhà cung cấp
- `AIAgent`: AI agents chuyên biệt
- `AGE`: Artificial Genesis Engine (AI điều phối trung tâm)

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "name": "string",
  "agentType": "InternalAgent | ExternalAgent | AIAgent | AGE",
  "status": "Active | Inactive | PendingApproval | Disabled",
  "contactInfo": {
    "email": "string",
    "phone": "string"
  },
  "capabilities": ["string"],
  "creationDate": "datetime (ISO8601)",
  "lastModifiedDate": "datetime (ISO8601)"
}
```

### 2. Project
**Mô tả**: Tập hợp các nhiệm vụ có kế hoạch để giải quyết Tension hoặc tận dụng cơ hội

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "name": "string",
  "description": "string",
  "status": "Planning | Active | OnHold | Completed | Cancelled",
  "priority": "Low | Medium | High | Critical",
  "startDate": "datetime",
  "endDate": "datetime",
  "budget": "number",
  "progress": "number (0-100)",
  "tags": ["string"]
}
```

### 3. Task
**Mô tả**: Đơn vị công việc cụ thể trong một Project

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "title": "string",
  "description": "string",
  "status": "ToDo | InProgress | Completed | Cancelled",
  "priority": "Low | Medium | High | Critical",
  "dueDate": "datetime",
  "effortEstimate": "integer (hours)",
  "actualEffort": "integer (hours)",
  "tags": ["string"]
}
```

### 4. WIN
**Mô tả**: Thành tựu, kết quả tích cực đạt được

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "title": "string",
  "description": "string",
  "impact": "Low | Medium | High | Critical",
  "category": "Process | Product | People | Performance",
  "valueCreated": "number",
  "achievementDate": "datetime",
  "tags": ["string"]
}
```

### 5. Recognition
**Mô tả**: Ghi nhận đóng góp, thành tựu của Agent hoặc WIN

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "name": "string",
  "message": "string",
  "recognitionType": "Achievement | Contribution | Milestone | Innovation",
  "recognitionDate": "datetime",
  "impactScore": "number (1-10)",
  "tags": ["string"]
}
```

### 6. Knowledge Snippet
**Mô tả**: Mảnh tri thức, kinh nghiệm được trích xuất

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "title": "string",
  "content": "string",
  "snippetType": "Insight | Lesson | Best Practice | Methodology",
  "confidenceScore": "number (0-1)",
  "source": "string",
  "tags": ["string"],
  "creationDate": "datetime"
}
```

### 7. Event
**Mô tả**: Ghi lại sự kiện quan trọng trong hệ thống

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "eventType": "string",
  "timestamp": "datetime",
  "description": "string",
  "source": "string",
  "status": "New | Processing | Processed | FailedToProcess | Archived",
  "metadata": "object",
  "actorAgentId": "string (UUID)",
  "targetEntityId": "string (UUID)",
  "targetEntityType": "string"
}
```

### 8. Tension
**Mô tả**: Vấn đề, cơ hội, hoặc sự không nhất quán cần giải quyết

**Key Properties**:
```json
{
  "uid": "string (UUID)",
  "title": "string",
  "description": "string",
  "status": "Open | InProgress | Resolved | Closed",
  "priority": "Low | Medium | High | Critical",
  "tensionType": "Problem | Opportunity | Risk | Question",
  "currentState": "string",
  "desiredState": "string",
  "impactAssessment": "string",
  "tags": ["string"]
}
```

---

## 🔗 Relationships

### Core Relationships

#### 1. GIVEN_BY
**Description**: Recognition được trao bởi Agent nào
```
Recognition -[GIVEN_BY]-> Agent
```

#### 2. RECEIVED_BY  
**Description**: Recognition được nhận bởi Agent nào
```
Recognition -[RECEIVED_BY]-> Agent
```

#### 3. RECOGNIZES_WIN
**Description**: Recognition công nhận WIN nào
```
Recognition -[RECOGNIZES_WIN]-> WIN
```

#### 4. GENERATES_KNOWLEDGE
**Description**: WIN tạo ra Knowledge Snippet nào
```
WIN -[GENERATES_KNOWLEDGE]-> KnowledgeSnippet
```

#### 5. LEADS_TO_WIN
**Description**: Project/Event dẫn đến WIN
```
Project -[LEADS_TO_WIN]-> WIN
Event -[LEADS_TO_WIN]-> WIN
```

#### 6. RESOLVES
**Description**: Task giải quyết Tension nào
```
Task -[RESOLVES]-> Tension
```

#### 7. ASSIGNED_TO
**Description**: Task được giao cho Agent nào
```
Task -[ASSIGNED_TO]-> Agent
```

#### 8. BELONGS_TO
**Description**: Task thuộc về Project nào
```
Task -[BELONGS_TO]-> Project
```

#### 9. MANAGES
**Description**: Agent quản lý Project nào
```
Agent -[MANAGES]-> Project
```

#### 10. PARTICIPATES_IN
**Description**: Agent tham gia Project nào
```
Agent -[PARTICIPATES_IN]-> Project
```

---

## 🚀 API Endpoints

### Entities CRUD Operations

#### Agents
```http
GET    /api/v1/agents/                    # List all agents
POST   /api/v1/agents/                    # Create new agent
GET    /api/v1/agents/{agent_id}          # Get agent by ID
PUT    /api/v1/agents/{agent_id}          # Update agent
DELETE /api/v1/agents/{agent_id}          # Delete agent
```

#### Projects
```http
GET    /api/v1/projects/                  # List all projects
POST   /api/v1/projects/                  # Create new project
GET    /api/v1/projects/{project_id}      # Get project by ID
PUT    /api/v1/projects/{project_id}      # Update project
DELETE /api/v1/projects/{project_id}      # Delete project
```

#### Tasks
```http
GET    /api/v1/tasks/                     # List all tasks
POST   /api/v1/tasks/                     # Create new task
GET    /api/v1/tasks/{task_id}            # Get task by ID
PUT    /api/v1/tasks/{task_id}            # Update task
DELETE /api/v1/tasks/{task_id}            # Delete task
```

#### WINs
```http
GET    /api/v1/wins/                      # List all WINs
POST   /api/v1/wins/                      # Create new WIN
GET    /api/v1/wins/{win_id}              # Get WIN by ID
PUT    /api/v1/wins/{win_id}              # Update WIN
DELETE /api/v1/wins/{win_id}              # Delete WIN
```

#### Recognitions
```http
GET    /api/v1/recognitions/              # List all recognitions
POST   /api/v1/recognitions/              # Create new recognition
GET    /api/v1/recognitions/{recognition_id}  # Get recognition by ID
PUT    /api/v1/recognitions/{recognition_id}  # Update recognition
DELETE /api/v1/recognitions/{recognition_id}  # Delete recognition
```

#### Knowledge Snippets
```http
GET    /api/v1/knowledge-snippets/        # List all snippets
POST   /api/v1/knowledge-snippets/        # Create new snippet
GET    /api/v1/knowledge-snippets/{snippet_id}  # Get snippet by ID
PUT    /api/v1/knowledge-snippets/{snippet_id}  # Update snippet
DELETE /api/v1/knowledge-snippets/{snippet_id}  # Delete snippet
```

#### Events
```http
GET    /api/v1/events/                    # List all events
POST   /api/v1/events/                    # Create new event
GET    /api/v1/events/{event_id}          # Get event by ID
PUT    /api/v1/events/{event_id}          # Update event
DELETE /api/v1/events/{event_id}          # Delete event
```

#### Tensions
```http
GET    /api/v1/tensions/                  # List all tensions
POST   /api/v1/tensions/                  # Create new tension
GET    /api/v1/tensions/{tension_id}      # Get tension by ID
PUT    /api/v1/tensions/{tension_id}      # Update tension
DELETE /api/v1/tensions/{tension_id}      # Delete tension
```

### Relationship Operations

#### Create Relationships
```http
POST /api/v1/recognitions/{recognition_id}/given-by/{agent_id}
POST /api/v1/recognitions/{recognition_id}/received-by/{agent_id}
POST /api/v1/recognitions/{recognition_id}/recognizes-win/{win_id}
POST /api/v1/wins/{win_id}/generates-knowledge/{snippet_id}
POST /api/v1/projects/{project_id}/leads-to-win/{win_id}
POST /api/v1/tasks/{task_id}/resolves/{tension_id}
POST /api/v1/tasks/{task_id}/assigned-to/{agent_id}
```

#### Delete Relationships
```http
DELETE /api/v1/recognitions/{recognition_id}/given-by/{agent_id}
DELETE /api/v1/recognitions/{recognition_id}/received-by/{agent_id}
DELETE /api/v1/recognitions/{recognition_id}/recognizes-win/{win_id}
DELETE /api/v1/wins/{win_id}/generates-knowledge/{snippet_id}
DELETE /api/v1/projects/{project_id}/leads-to-win/{win_id}
DELETE /api/v1/tasks/{task_id}/resolves/{tension_id}
DELETE /api/v1/tasks/{task_id}/assigned-to/{agent_id}
```

#### Query Relationships
```http
GET /api/v1/recognitions/{recognition_id}/given-by
GET /api/v1/recognitions/{recognition_id}/received-by
GET /api/v1/recognitions/{recognition_id}/wins
GET /api/v1/wins/{win_id}/knowledge-snippets
GET /api/v1/projects/{project_id}/wins
GET /api/v1/tasks/{task_id}/tensions
GET /api/v1/agents/{agent_id}/tasks
```

### Specialized Endpoints

#### Agent-centric Views
```http
GET /api/v1/agents/{agent_id}/recognitions/given      # Recognitions given by agent
GET /api/v1/agents/{agent_id}/recognitions/received   # Recognitions received by agent
GET /api/v1/agents/{agent_id}/projects/managed        # Projects managed by agent
GET /api/v1/agents/{agent_id}/projects/participated   # Projects participated by agent
GET /api/v1/agents/{agent_id}/tasks/assigned          # Tasks assigned to agent
```

#### Project-centric Views
```http
GET /api/v1/projects/{project_id}/tasks               # All tasks in project
GET /api/v1/projects/{project_id}/agents              # All agents in project
GET /api/v1/projects/{project_id}/wins                # WINs achieved by project
GET /api/v1/projects/{project_id}/tensions            # Tensions addressed by project
```

#### WIN-centric Views
```http
GET /api/v1/wins/{win_id}/recognitions                # Recognitions for this WIN
GET /api/v1/wins/{win_id}/projects                    # Projects that led to this WIN
GET /api/v1/wins/{win_id}/knowledge-snippets          # Knowledge generated from WIN
```

### Query Parameters

#### Pagination
```http
?skip=0&limit=100
```

#### Filtering
```http
?status=Active
?priority=High
?tags=innovation,ai
?date_from=2024-01-01&date_to=2024-12-31
```

#### Sorting
```http
?sort_by=creationDate&sort_order=desc
```

#### Include Related Data
```http
?include=relationships
?include=metadata
?include=full_details
```

---

## 📊 Data Models

### Request/Response Format

#### Standard List Response
```json
{
  "items": [
    {
      "uid": "uuid",
      "name": "string",
      // ... entity properties
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 100,
  "has_more": true
}
```

#### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "name",
      "issue": "required field missing"
    },
    "request_id": "req_123456789"
  }
}
```

#### Relationship Response
```json
{
  "relationship": {
    "source_id": "uuid",
    "source_type": "Recognition",
    "target_id": "uuid", 
    "target_type": "Agent",
    "relationship_type": "GIVEN_BY",
    "properties": {
      "created_at": "datetime",
      "notes": "string"
    }
  }
}
```

### Data Validation Rules

#### Required Fields
- All entities must have: `name`, `status`
- UUIDs are auto-generated if not provided
- Timestamps are auto-set to current time

#### Field Constraints
- `name`: 1-255 characters
- `description`: max 2000 characters
- `status`: must be from predefined enum
- `priority`: must be from predefined enum
- `email`: valid email format
- `dates`: ISO 8601 format

#### Business Rules
- Agent cannot be deleted if has active relationships
- Project status cannot go backwards (Active → Planning)
- Recognition must have both giver and receiver
- WIN must be linked to at least one Project or Event

---

## ⚠️ Error Handling

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `422`: Validation Error
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {
      "field": "specific_field",
      "value": "invalid_value",
      "constraint": "validation_rule"
    },
    "request_id": "req_123456789",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Input validation failed
- `NOT_FOUND`: Resource not found
- `DUPLICATE_ENTITY`: Entity already exists
- `RELATIONSHIP_EXISTS`: Relationship already established
- `RELATIONSHIP_NOT_FOUND`: Relationship does not exist
- `INVALID_TRANSITION`: Invalid status transition
- `DEPENDENCY_EXISTS`: Cannot delete due to dependencies
- `RATE_LIMIT_EXCEEDED`: Too many requests

---

## 🚦 Rate Limiting

### Limits
- **Standard**: 1000 requests/hour
- **Burst**: 100 requests/minute
- **Heavy Operations**: 10 requests/minute

### Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### Rate Limit Response
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "retry_after": 60
  }
}
```

---

## 💡 Examples

### Create Recognition Flow
```bash
# 1. Create Recognition
curl -X POST http://localhost:8000/api/v1/recognitions/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Outstanding AI Implementation",
    "message": "Excellent work on implementing the new AI agent system",
    "recognitionType": "Achievement"
  }'

# Response: {"uid": "rec_123", ...}

# 2. Link to Giver
curl -X POST http://localhost:8000/api/v1/recognitions/rec_123/given-by/agent_456

# 3. Link to Receiver  
curl -X POST http://localhost:8000/api/v1/recognitions/rec_123/received-by/agent_789

# 4. Link to WIN
curl -X POST http://localhost:8000/api/v1/recognitions/rec_123/recognizes-win/win_101
```

### Query Agent's Recognition History
```bash
# Get all recognitions received by agent
curl http://localhost:8000/api/v1/agents/agent_789/recognitions/received

# Get all recognitions given by agent
curl http://localhost:8000/api/v1/agents/agent_456/recognitions/given
```

### Create Project with Tasks
```bash
# 1. Create Project
curl -X POST http://localhost:8000/api/v1/projects/ \
  -d '{
    "name": "AI Agent Development",
    "description": "Develop intelligent agents for TRM-OS",
    "status": "Active",
    "priority": "High"
  }'

# 2. Create Task
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -d '{
    "title": "Design Agent Architecture",
    "description": "Create the foundational architecture for AI agents",
    "status": "ToDo",
    "priority": "High"
  }'

# 3. Link Task to Project
curl -X POST http://localhost:8000/api/v1/tasks/task_123/belongs-to/project_456

# 4. Assign Task to Agent
curl -X POST http://localhost:8000/api/v1/tasks/task_123/assigned-to/agent_789
```

---

## 🔄 Migration to v2

### Deprecation Timeline
- **v1.0**: Current stable version
- **v1.1**: Final v1 version with deprecation warnings
- **v2.0**: New major version (Q2 2025)
- **v1 EOL**: End of life 6 months after v2.0 release

### Breaking Changes in v2
- **Authentication**: OAuth 2.0 required
- **Endpoints**: GraphQL support added
- **Real-time**: WebSocket endpoints
- **Filtering**: Advanced query language
- **Pagination**: Cursor-based pagination

### Migration Tools
- **Data Export**: `GET /api/v1/export/full`
- **Schema Validation**: `POST /api/v2/validate/v1-data`
- **Migration Script**: `scripts/migrate_v1_to_v2.py`

### Backward Compatibility
- v1 endpoints will remain available for 6 months
- Gradual migration path with dual support
- Migration assistance tools and documentation

---

## 📚 Additional Resources

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: [Download](https://api.trm-os.com/postman)

### SDKs & Libraries
- **Python SDK**: `pip install trm-os-python`
- **JavaScript SDK**: `npm install trm-os-js`
- **CLI Tool**: `pip install trm-os-cli`

### Support
- **GitHub Issues**: [Report bugs](https://github.com/trm-os/trm-os-branches/issues)
- **Documentation**: [Full docs](https://docs.trm-os.com)
- **Community**: [Discord](https://discord.gg/trm-os)
- **Email**: api-support@trm-os.com

---

*This documentation is automatically generated from the OpenAPI specification and updated with each release.* 