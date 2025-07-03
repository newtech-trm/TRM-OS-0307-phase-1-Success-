# API Endpoints theo Ontology V3.2

Tài liệu này mô tả các API endpoints đã triển khai theo đúng Ontology V3.2 với tập trung vào các mối quan hệ quan trọng.

Lưu ý: Tất cả API endpoints đều sử dụng `camelCase` cho các tham số và thuộc tính theo quy ước chung của project.

## Mục lục

1. [Tension-Task Relationships](#tension-task-relationships)
2. [Tension-WIN Relationships](#tension-win-relationships)
3. [Task Comprehensive Views](#task-comprehensive-views)
4. [Tension Comprehensive Views](#tension-comprehensive-views)

---

## Tension-Task Relationships

### Connect Task to Tension (RESOLVES)

**Endpoint:** `POST /api/v1/tasks/{task_id}/resolves/{tension_id}`

**Description:** Thiết lập mối quan hệ RESOLVES từ một Task đến một Tension, thể hiện rằng Task này được tạo để giải quyết Tension.

**Path Parameters:**
- `task_id` (string, required): Định danh duy nhất của Task
- `tension_id` (string, required): Định danh duy nhất của Tension

**Response:**

- 201 Created:
  ```json
  {
    "detail": "Task {task_id} now resolves Tension {tension_id}"
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Could not establish relationship. Either Task or Tension not found."
  }
  ```

### Disconnect Task from Tension

**Endpoint:** `DELETE /api/v1/tasks/{task_id}/resolves/{tension_id}`

**Description:** Gỡ bỏ mối quan hệ RESOLVES giữa Task và Tension.

**Path Parameters:**
- `task_id` (string, required): Định danh duy nhất của Task
- `tension_id` (string, required): Định danh duy nhất của Tension

**Response:**

- 200 OK:
  ```json
  {
    "detail": "Task {task_id} no longer resolves Tension {tension_id}"
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Could not remove relationship. Either Task or Tension not found, or no relationship exists."
  }
  ```

### Get Tensions Resolved by Task

**Endpoint:** `GET /api/v1/tasks/{task_id}/resolves`

**Description:** Lấy danh sách tất cả các Tensions được giải quyết bởi một Task cụ thể.

**Path Parameters:**
- `task_id` (string, required): Định danh duy nhất của Task

**Query Parameters:**
- `skip` (integer, optional, default=0): Số lượng items cần bỏ qua
- `limit` (integer, optional, default=100): Số lượng tối đa items trả về

**Response:**

- 200 OK:
  ```json
  [
    {
      "uid": "tension-uuid-1",
      "title": "Need to improve API documentation",
      "description": "The API documentation is outdated and incomplete",
      "status": "Open",
      "priority": 2,
      "source": "FounderInput",
      "tensionType": "Problem",
      "currentState": "Documentation is hard to follow",
      "desiredState": "Clear, comprehensive documentation",
      "impactAssessment": "Medium impact on developer productivity",
      "tags": ["documentation", "api", "improvement"]
    }
  ]
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Task not found"
  }
  ```

---

## Tension-WIN Relationships

### Connect Tension to WIN (LEADS_TO_WIN)

**Endpoint:** `POST /api/v1/tensions/{tension_id}/leads-to-win/{win_id}`

**Description:** Thiết lập mối quan hệ LEADS_TO_WIN từ một Tension đến một WIN, thể hiện rằng Tension này đã dẫn đến hoặc đóng góp vào WIN.

**Path Parameters:**
- `tension_id` (string, required): Định danh duy nhất của Tension
- `win_id` (string, required): Định danh duy nhất của WIN

**Query Parameters:**
- `contribution_level` (integer, optional, default=3): Mức độ đóng góp, từ 1 (thấp) đến 5 (cao)
- `direct_contribution` (boolean, optional, default=true): Xác định liệu Tension có trực tiếp dẫn đến WIN hay không

**Response:**

- 201 Created:
  ```json
  {
    "detail": "Tension {tension_id} now leads to WIN {win_id}"
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Could not establish relationship. Either Tension or WIN not found."
  }
  ```

### Disconnect Tension from WIN

**Endpoint:** `DELETE /api/v1/tensions/{tension_id}/leads-to-win/{win_id}`

**Description:** Gỡ bỏ mối quan hệ LEADS_TO_WIN giữa Tension và WIN.

**Path Parameters:**
- `tension_id` (string, required): Định danh duy nhất của Tension
- `win_id` (string, required): Định danh duy nhất của WIN

**Response:**

- 200 OK:
  ```json
  {
    "detail": "Tension {tension_id} no longer leads to WIN {win_id}"
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Could not remove relationship. Either Tension or WIN not found, or no relationship exists."
  }
  ```

### Get WINs Led by Tension

**Endpoint:** `GET /api/v1/tensions/{tension_id}/leads-to-win`

**Description:** Lấy danh sách tất cả các WINs mà một Tension cụ thể đã dẫn đến.

**Path Parameters:**
- `tension_id` (string, required): Định danh duy nhất của Tension

**Query Parameters:**
- `skip` (integer, optional, default=0): Số lượng items cần bỏ qua
- `limit` (integer, optional, default=100): Số lượng tối đa items trả về

**Response:**

- 200 OK:
  ```json
  [
    {
      "uid": "win-uuid-1",
      "title": "Improved API documentation coverage",
      "description": "Comprehensive API documentation for all endpoints",
      "impact": "High",
      "category": "Process",
      "valueCreated": 50000
    }
  ]
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Tension not found"
  }
  ```

---

## Task Comprehensive Views

### Get Task with All Relationships

**Endpoint:** `GET /api/v1/tasks/{task_id}/with-relationships`

**Description:** Lấy thông tin đầy đủ về một Task kèm theo tất cả các mối quan hệ của nó (project, assignees, tensions, v.v.)

**Path Parameters:**
- `task_id` (string, required): Định danh duy nhất của Task

**Response:**

- 200 OK:
  ```json
  {
    "task": {
      "uid": "task-uuid-1",
      "title": "Update API documentation",
      "description": "Create comprehensive API documentation for all endpoints",
      "status": "InProgress",
      "priority": 2,
      "estimatedEffort": 4.5,
      "dueDate": "2025-07-15T00:00:00Z"
    },
    "project": {
      "uid": "project-uuid-1",
      "name": "API Improvement Project",
      "description": "Project to improve API quality and documentation"
    },
    "created_by": {
      "uid": "agent-uuid-1",
      "name": "Documentation Bot",
      "type": "AI"
    },
    "assignees": {
      "users": [
        {
          "uid": "user-uuid-1",
          "name": "John Developer",
          "email": "john@example.com",
          "assignment_type": "Primary",
          "priority_level": 2,
          "assigned_at": "2025-07-01T10:15:30Z"
        }
      ],
      "agents": []
    },
    "resolves_tensions": [
      {
        "uid": "tension-uuid-1",
        "title": "Need to improve API documentation",
        "description": "The API documentation is outdated and incomplete",
        "status": "Open",
        "priority": 2,
        "source": "FounderInput"
      }
    ]
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Task not found"
  }
  ```

---

## Tension Comprehensive Views

### Get Tension with All Relationships

**Endpoint:** `GET /api/v1/tensions/{tension_id}/with-relationships`

**Description:** Lấy thông tin đầy đủ về một Tension kèm theo tất cả các mối quan hệ của nó (projects, tasks, wins, v.v.)

**Path Parameters:**
- `tension_id` (string, required): Định danh duy nhất của Tension

**Response:**

- 200 OK:
  ```json
  {
    "tension": {
      "uid": "tension-uuid-1",
      "title": "Need to improve API documentation",
      "description": "The API documentation is outdated and incomplete",
      "status": "Open",
      "priority": 2,
      "source": "FounderInput",
      "tensionType": "Problem",
      "currentState": "Documentation is hard to follow",
      "desiredState": "Clear, comprehensive documentation",
      "impactAssessment": "Medium impact on developer productivity",
      "tags": ["documentation", "api", "improvement"]
    },
    "reported_by": {
      "uid": "agent-uuid-2",
      "name": "Quality Control Bot",
      "type": "AI"
    },
    "owned_by": {
      "uid": "user-uuid-2",
      "name": "Sarah Manager",
      "email": "sarah@example.com"
    },
    "affects_projects": [
      {
        "uid": "project-uuid-1",
        "name": "API Improvement Project",
        "description": "Project to improve API quality and documentation"
      }
    ],
    "resolved_by_tasks": [
      {
        "uid": "task-uuid-1",
        "title": "Update API documentation",
        "description": "Create comprehensive API documentation for all endpoints",
        "status": "InProgress",
        "priority": 2
      }
    ],
    "leads_to_wins": [
      {
        "uid": "win-uuid-1",
        "title": "Improved API documentation coverage",
        "description": "Comprehensive API documentation for all endpoints",
        "impact": "High",
        "category": "Process",
        "valueCreated": 50000
      }
    ]
  }
  ```

- 404 Not Found:
  ```json
  {
    "detail": "Tension not found"
  }
  ```
