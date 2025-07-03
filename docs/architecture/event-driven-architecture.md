# Event-Driven Architecture trong TRM-OS

## Tổng quan

TRM-OS sử dụng kiến trúc event-driven làm nền tảng cho giao tiếp giữa các thành phần, đặc biệt là giữa các AI Agent. Kiến trúc này cho phép các thành phần hoạt động độc lập và phản ứng với các sự kiện trong hệ thống một cách không đồng bộ.

## SystemEventBus

Cốt lõi của kiến trúc event-driven trong TRM-OS là module `SystemEventBus`.

### Đặc điểm chính

- **Singleton pattern**: Một instance duy nhất trong toàn bộ hệ thống
- **Publish-Subscribe model**: Các thành phần có thể đăng ký nhận các loại sự kiện cụ thể
- **Async/await support**: Tất cả các phương thức đều là async để hỗ trợ xử lý đồng thời
- **Event history**: Lưu trữ lịch sử sự kiện để truy vết và phân tích

### Ví dụ triển khai

```python
class SystemEventBus:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemEventBus, cls).__new__(cls)
            cls._instance._subscribers = defaultdict(list)
            cls._instance._event_history = []
        return cls._instance
    
    async def publish(self, event_type: EventType, data: dict = None, metadata: dict = None):
        """Publish an event to all subscribers of this event type"""
        event = {
            "type": event_type,
            "data": data or {},
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self._event_history.append(event)
        
        subscribers = self._subscribers.get(event_type, [])
        if subscribers:
            await asyncio.gather(*[subscriber(event) for subscriber in subscribers])
        
        return event
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to a specific event type"""
        self._subscribers[event_type].append(callback)
        
        # Return unsubscribe function
        def unsubscribe():
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
        
        return unsubscribe
```

## EventType Enum

Các loại sự kiện trong hệ thống được định nghĩa bằng enum `EventType` theo đúng ontology:

```python
class EventType(str, Enum):
    TENSION_CREATED = "tensionCreated"
    TENSION_UPDATED = "tensionUpdated"
    TENSION_RESOLVED = "tensionResolved"
    
    TASK_CREATED = "taskCreated"
    TASK_ASSIGNED = "taskAssigned"
    TASK_STARTED = "taskStarted"
    TASK_COMPLETED = "taskCompleted"
    
    PROJECT_CREATED = "projectCreated"
    PROJECT_UPDATED = "projectUpdated"
    PROJECT_COMPLETED = "projectCompleted"
    
    WIN_CREATED = "winCreated"
    
    AGENT_ACTIVATED = "agentActivated"
    AGENT_DEACTIVATED = "agentDeactivated"
```

## BaseAgent và Event Handling

Các AI Agent trong hệ thống kế thừa từ `BaseAgent` và xử lý các sự kiện thông qua SystemEventBus:

```python
class BaseAgent:
    def __init__(self, agent_id: str, agent_type: str, metadata: AgentMetadata = None):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.metadata = metadata or AgentMetadata()
        self.event_bus = SystemEventBus()
        self._active = False
        self._subscriptions = []
    
    async def initialize(self):
        """Initialize agent resources"""
        pass
    
    async def start(self):
        """Start the agent and register event handlers"""
        if not self._active:
            self._active = True
            self._register_event_handlers()
            await self.event_bus.publish(
                EventType.AGENT_ACTIVATED,
                {"agent_id": self.agent_id, "agent_type": self.agent_type}
            )
    
    async def stop(self):
        """Stop the agent and unregister event handlers"""
        if self._active:
            self._active = False
            # Unsubscribe from all events
            for unsubscribe in self._subscriptions:
                unsubscribe()
            self._subscriptions = []
            await self.event_bus.publish(
                EventType.AGENT_DEACTIVATED,
                {"agent_id": self.agent_id, "agent_type": self.agent_type}
            )
    
    def _register_event_handlers(self):
        """Register event handlers for this agent"""
        raise NotImplementedError("Subclasses must implement this method")
    
    async def handle_event(self, event):
        """Base event handler method"""
        raise NotImplementedError("Subclasses must implement this method")
```

## Ví dụ: ResolutionCoordinatorAgent

`ResolutionCoordinatorAgent` là một ví dụ về việc triển khai agent sử dụng event-driven architecture:

```python
class ResolutionCoordinatorAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            agent_type="ResolutionCoordinator",
            metadata=AgentMetadata(
                name="Resolution Coordinator",
                description="Coordinates resolution process for tensions"
            )
        )
        self.tension_service = TensionService()
    
    async def initialize(self):
        """Initialize by loading unresolved tensions"""
        self.unresolved_tensions = await self.tension_service.get_unresolved_tensions()
    
    def _register_event_handlers(self):
        """Register for tension-related events"""
        self._subscriptions = [
            self.event_bus.subscribe(EventType.TENSION_CREATED, self.handle_tension_created),
            self.event_bus.subscribe(EventType.TENSION_UPDATED, self.handle_tension_updated),
            self.event_bus.subscribe(EventType.PROJECT_CREATED, self.handle_project_created)
        ]
    
    async def handle_tension_created(self, event):
        """Handle newly created tensions"""
        tension_data = event.get("data", {})
        tension_uid = tension_data.get("uid")
        
        if not tension_uid:
            return
        
        tension = await self.tension_service.get_tension(tension_uid)
        self.unresolved_tensions.append(tension)
        
        # Initiate resolution process
        await self._start_resolution_process(tension)
```

## Kết nối với API Layer

API endpoints có thể kích hoạt các sự kiện thông qua SystemEventBus:

```python
@router.post("/tensions/", response_model=TensionResponseSchema)
@adapt_tension_response
async def create_tension(tension: TensionCreateSchema, service: TensionService = Depends(get_tension_service)):
    """Create a new tension"""
    tension_data = await service.create_tension(tension.dict())
    
    # Publish event after successful creation
    event_bus = SystemEventBus()
    await event_bus.publish(
        EventType.TENSION_CREATED,
        {"uid": tension_data["uid"]}
    )
    
    return tension_data
```

## Lợi ích của kiến trúc Event-Driven

1. **Decoupling**: Các thành phần hoạt động độc lập, giảm phụ thuộc trực tiếp
2. **Scalability**: Dễ dàng mở rộng hệ thống bằng cách thêm các subscriber mới
3. **Flexibility**: Có thể thêm hoặc thay đổi logic xử lý sự kiện mà không ảnh hưởng đến các thành phần khác
4. **Traceability**: Lịch sử sự kiện giúp dễ dàng debug và phân tích

## Giai đoạn tiếp theo

Trong các giai đoạn tiếp theo, cần phát triển:

1. **Persistence cho event history**: Lưu trữ lịch sử sự kiện vào database để hỗ trợ recovery và analytics
2. **Event schema validation**: Xác thực dữ liệu sự kiện dựa trên schema
3. **Distributed event processing**: Mở rộng để hỗ trợ xử lý sự kiện phân tán (với Kafka hoặc RabbitMQ)
4. **Event monitoring dashboard**: Giao diện theo dõi và quản lý các sự kiện trong hệ thống

## Tham khảo

- [Ontology-First Approach](./ontology-first-approach.md)
- [Async API Pattern](../technical-decisions/async-api-pattern.md)
- [Agent Ecosystem](../roadmap/phase-2-agent-ecosystem.md)
