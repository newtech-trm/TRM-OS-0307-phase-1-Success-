# KẾ HOẠCH CHUẨN HÓA CẤU TRÚC DỰ ÁN TRM-OS
## "Ontology-First Architecture Standardization"

**Phiên bản:** 1.0  
**Ngày tạo:** 2025-07-06  
**Mục đích:** Chuẩn hóa toàn bộ cấu trúc dự án theo nguyên tắc Ontology-First và Event-Driven Architecture

---

## PHẦN I: PHÂN TÍCH HIỆN TRẠNG

### 1. CẤU TRÚC HIỆN TẠI (v1.0)

#### 1.1. Điểm Mạnh ✅
```
trm-os-branches/
├── trm_api/                    # Core API well-structured
│   ├── models/                 # ✅ Pydantic models hoàn chỉnh
│   ├── graph_models/           # ✅ Neo4j ontology entities
│   ├── api/v1/endpoints/       # ✅ RESTful endpoints
│   ├── eventbus/               # ✅ Event-driven communication
│   ├── repositories/           # ✅ Data access layer
│   ├── adapters/               # ✅ Data transformation
│   └── services/               # ✅ Business logic
├── tests/                      # ✅ 218 comprehensive tests
├── docs/                       # ✅ Rich documentation
└── scripts/                    # ✅ Utility scripts
```

#### 1.2. Vấn đề Cần Giải Quyết 🚨
1. **Thiếu Agent Layer**: Chưa có cấu trúc rõ ràng cho AI Agents
2. **Ontology Fragmentation**: Graph models và Pydantic models không sync
3. **Missing Genesis Engine**: Chưa có cơ chế quản lý Agent lifecycle
4. **No Reasoning Layer**: Chưa có AI reasoning capabilities
5. **Limited HMI**: Chưa có Human-Machine Interface layer

### 2. TARGET ARCHITECTURE (v2.0)

#### 2.1. Cấu trúc Mục tiêu
```
trm-os-v2/
├── trm_core/                   # 🆕 Core ontology & shared utilities
│   ├── ontology/               # Central ontology definitions
│   ├── events/                 # Event schemas & types
│   ├── patterns/               # Design patterns & base classes
│   └── utils/                  # Shared utilities
├── trm_agents/                 # 🆕 AI Agent ecosystem
│   ├── genesis/                # Genesis Engine
│   ├── reasoning/              # Reasoning agents
│   ├── execution/              # Execution agents
│   ├── sense/                  # Sense agents
│   └── integration/            # Integration agents
├── trm_api/                    # Enhanced API layer
│   ├── v1/                     # Legacy API (maintained)
│   ├── v2/                     # 🆕 Event-driven API
│   └── shared/                 # Shared API components
├── trm_hmi/                    # 🆕 Human-Machine Interface
│   ├── dashboard/              # Strategic dashboard
│   ├── conversation/           # Conversational interface
│   └── visualization/          # Data visualization
├── trm_intelligence/           # 🆕 AI Intelligence layer
│   ├── quantum_states/         # 4 Quantum WIN states
│   ├── pattern_detection/      # Pattern recognition
│   └── learning/               # Machine learning models
└── tests/                      # Enhanced testing framework
    ├── unit/                   # Unit tests
    ├── integration/            # Integration tests
    ├── agents/                 # Agent behavior tests
    └── e2e/                    # End-to-end tests
```

---

## PHẦN II: MIGRATION STRATEGY

### 3. GIAI ĐOẠN 1: CORE REFACTORING (Tuần 1-2)

#### 3.1. Tạo trm_core Package
```bash
# Tạo cấu trúc core
mkdir -p trm_core/{ontology,events,patterns,utils}

# Di chuyển ontology definitions
mv trm_api/graph_models/* trm_core/ontology/
mv trm_api/eventbus/* trm_core/events/
```

#### 3.2. Standardize Ontology Definitions
```python
# trm_core/ontology/base.py
from abc import ABC, abstractmethod
from neomodel import StructuredNode
from pydantic import BaseModel

class OntologyEntity(ABC):
    """Base class cho tất cả ontology entities"""
    
    @abstractmethod
    def to_graph_model(self) -> StructuredNode:
        """Convert to Neo4j graph model"""
        pass
    
    @abstractmethod  
    def to_pydantic_model(self) -> BaseModel:
        """Convert to Pydantic model"""
        pass
    
    @abstractmethod
    def validate_constraints(self) -> bool:
        """Validate ontology constraints"""
        pass
```

#### 3.3. Create Universal Event Schema
```python
# trm_core/events/schema.py
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class EventCategory(str, Enum):
    SYSTEM = "system"
    AGENT = "agent" 
    USER = "user"
    EXTERNAL = "external"

class UniversalEvent(BaseModel):
    """Universal event schema cho toàn bộ hệ thống"""
    event_id: str = Field(default_factory=generate_event_id)
    category: EventCategory
    event_type: str
    source_entity_id: str
    target_entity_ids: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None  # For event chains
    win_impact: Optional[Dict[str, float]] = None  # W, I, N scores
```

### 4. GIAI ĐOẠN 2: AGENT ECOSYSTEM (Tuần 3-4)

#### 4.1. Implement BaseAgent Pattern
```python
# trm_core/patterns/base_agent.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from trm_core.events.schema import UniversalEvent
from trm_core.ontology.base import OntologyEntity

class BaseAgent(OntologyEntity, ABC):
    """Base class cho tất cả AI Agents trong TRM-OS"""
    
    def __init__(self, agent_id: str, name: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.status = "initializing"
        self.win_score = 0.0
        
    @abstractmethod
    async def process_event(self, event: UniversalEvent) -> Optional[UniversalEvent]:
        """Process incoming event and optionally return response event"""
        pass
    
    @abstractmethod
    async def get_health_status(self) -> Dict[str, Any]:
        """Return agent health and performance metrics"""
        pass
    
    async def evolve(self, feedback: Dict[str, Any]) -> None:
        """Learn and evolve based on feedback"""
        # Default implementation - can be overridden
        pass
```

#### 4.2. Create Genesis Engine
```python
# trm_agents/genesis/engine.py
from typing import List, Dict, Any
from trm_core.patterns.base_agent import BaseAgent
from trm_core.events.schema import UniversalEvent
from trm_api.models.tension import Tension

class GenesisEngine:
    """Cỗ máy tạo và quản lý lifecycle của Agents"""
    
    def __init__(self):
        self.active_agents: Dict[str, BaseAgent] = {}
        self.agent_templates: Dict[str, type] = {}
        self.performance_metrics: Dict[str, float] = {}
    
    async def analyze_tension(self, tension: Tension) -> List[str]:
        """Phân tích tension và xác định agents cần thiết"""
        required_capabilities = []
        
        # AI logic to determine required capabilities
        if "data" in tension.description.lower():
            required_capabilities.append("data_analysis")
        if "code" in tension.description.lower():
            required_capabilities.append("code_generation")
        if "user" in tension.description.lower():
            required_capabilities.append("user_interaction")
            
        return required_capabilities
    
    async def create_agent(self, capabilities: List[str], purpose: str) -> BaseAgent:
        """Tạo agent mới với capabilities cụ thể"""
        # Select best agent template
        agent_type = self._select_agent_type(capabilities)
        
        # Create agent instance
        agent = agent_type(
            agent_id=generate_agent_id(),
            name=f"{agent_type.__name__}_{timestamp()}",
            capabilities=capabilities
        )
        
        # Register agent
        self.active_agents[agent.agent_id] = agent
        
        # Publish creation event
        await self._publish_agent_created_event(agent)
        
        return agent
    
    async def evolve_agent(self, agent_id: str, performance_data: Dict[str, Any]) -> None:
        """Tiến hóa agent dựa trên performance"""
        agent = self.active_agents.get(agent_id)
        if not agent:
            return
            
        # Calculate WIN score
        win_score = self._calculate_win_score(performance_data)
        
        # Decide evolution strategy
        if win_score < 0.3:
            await self._retire_agent(agent)
        elif win_score > 0.8:
            await self._enhance_agent(agent)
        
    async def manage_ecosystem(self) -> None:
        """Quản lý toàn bộ ecosystem của agents"""
        # Monitor agent health
        # Balance workload
        # Optimize resource allocation
        # Detect collaboration opportunities
        pass
```

### 5. GIAI ĐOẠN 3: REASONING LAYER (Tuần 5-6)

#### 5.1. Implement Reasoning Agents
```python
# trm_agents/reasoning/analyzer.py
from typing import List, Dict, Any
from trm_core.patterns.base_agent import BaseAgent
from trm_api.models.tension import Tension

class TensionAnalyzer(BaseAgent):
    """Agent chuyên phân tích tensions và đề xuất giải pháp"""
    
    async def analyze_tension(self, tension: Tension) -> List[Dict[str, Any]]:
        """Phân tích tension và đề xuất solutions"""
        solutions = []
        
        # 1. Root cause analysis
        root_causes = await self._identify_root_causes(tension)
        
        # 2. Solution generation
        for cause in root_causes:
            solution = await self._generate_solution(cause, tension)
            solutions.append(solution)
        
        # 3. Solution ranking
        ranked_solutions = await self._rank_solutions(solutions, tension)
        
        return ranked_solutions
    
    async def _identify_root_causes(self, tension: Tension) -> List[str]:
        """Identify root causes using AI analysis"""
        # Implement AI logic for root cause analysis
        # Could use LLM, rule-based system, or ML model
        pass
    
    async def _generate_solution(self, cause: str, tension: Tension) -> Dict[str, Any]:
        """Generate solution for specific root cause"""
        # Implement solution generation logic
        pass
    
    async def _rank_solutions(self, solutions: List[Dict], tension: Tension) -> List[Dict]:
        """Rank solutions by WIN potential"""
        # Implement solution ranking algorithm
        pass
```

#### 5.2. Implement Simulation Engine
```python
# trm_agents/reasoning/simulator.py
from typing import Dict, Any, List
from trm_core.patterns.base_agent import BaseAgent

class OutcomeSimulator(BaseAgent):
    """Agent chuyên mô phỏng kết quả của các hành động"""
    
    async def simulate_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Mô phỏng kết quả của một solution"""
        simulation_result = {
            "success_probability": 0.0,
            "win_impact": {"wisdom": 0.0, "intelligence": 0.0, "networking": 0.0},
            "resource_cost": {"time": 0, "cpu": 0, "human_effort": 0},
            "risks": [],
            "side_effects": []
        }
        
        # Run simulation models
        simulation_result["success_probability"] = await self._calculate_success_probability(solution, context)
        simulation_result["win_impact"] = await self._calculate_win_impact(solution, context)
        simulation_result["resource_cost"] = await self._estimate_resource_cost(solution)
        simulation_result["risks"] = await self._identify_risks(solution, context)
        
        return simulation_result
```

### 6. GIAI ĐOẠN 4: API V2 IMPLEMENTATION (Tuần 7-8)

#### 6.1. Create API v2 Structure
```python
# trm_api/v2/main.py
from fastapi import FastAPI, WebSocket
from trm_api.v2.endpoints import events, tensions, projects, agents, quantum_states

app = FastAPI(title="TRM-OS API v2", version="2.0.0")

# Event-driven endpoints
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(tensions.router, prefix="/tensions", tags=["Tensions"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"]) 
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(quantum_states.router, prefix="/quantum-states", tags=["Quantum States"])

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time event streaming"""
    await websocket.accept()
    # Implement WebSocket logic for real-time communication
```

#### 6.2. Event-Driven Endpoints
```python
# trm_api/v2/endpoints/events.py
from fastapi import APIRouter, HTTPException
from trm_core.events.schema import UniversalEvent
from trm_agents.genesis.engine import GenesisEngine

router = APIRouter()
genesis_engine = GenesisEngine()

@router.post("/", response_model=Dict[str, str])
async def submit_event(event: UniversalEvent):
    """Submit event to TRM-OS for processing"""
    try:
        # Validate event
        await event.validate()
        
        # Route to appropriate agents
        await genesis_engine.route_event(event)
        
        # Return acknowledgment
        return {
            "event_id": event.event_id,
            "status": "accepted",
            "message": "Event submitted for processing"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{event_id}/status")
async def get_event_status(event_id: str):
    """Get processing status of an event"""
    # Implementation for tracking event processing
    pass
```

---

## PHẦN III: IMPLEMENTATION GUIDELINES

### 7. CODING STANDARDS

#### 7.1. Ontology-First Development
```python
# 1. Define in ontology first
# trm_core/ontology/entities/reasoning_agent.py
class ReasoningAgentEntity(OntologyEntity):
    entity_type = "ReasoningAgent"
    required_properties = ["reasoning_type", "confidence_threshold"]
    
# 2. Generate graph model
# trm_core/ontology/graph_models/reasoning_agent.py  
class ReasoningAgentNode(StructuredNode):
    # Auto-generated from ontology
    pass

# 3. Generate Pydantic model
# trm_api/models/reasoning_agent.py
class ReasoningAgent(BaseModel):
    # Auto-generated from ontology
    pass
```

#### 7.2. Event-Driven Communication
```python
# All important changes must generate events
async def create_agent(self, capabilities: List[str]) -> Agent:
    agent = Agent(capabilities=capabilities)
    
    # Save to database
    await self.repository.create(agent)
    
    # Publish event
    await publish_event(
        event_type="agent.created",
        source_entity_id="genesis_engine",
        payload={"agent_id": agent.id, "capabilities": capabilities}
    )
    
    return agent
```

#### 7.3. WIN-Oriented Design
```python
# Every action should calculate WIN impact
class ActionResult:
    success: bool
    win_impact: WinImpact
    resource_cost: ResourceCost
    side_effects: List[str]

class WinImpact:
    wisdom_gain: float  # -1.0 to 1.0
    intelligence_gain: float
    networking_gain: float
    
    @property
    def total_score(self) -> float:
        return (self.wisdom_gain + self.intelligence_gain + self.networking_gain) / 3
```

### 8. TESTING STRATEGY

#### 8.1. Test Structure
```
tests/
├── unit/
│   ├── test_ontology_entities.py
│   ├── test_agents/
│   ├── test_reasoning/
│   └── test_events/
├── integration/
│   ├── test_agent_collaboration.py
│   ├── test_event_flows.py
│   └── test_api_v2.py
├── agents/
│   ├── test_genesis_engine.py
│   ├── test_reasoning_quality.py
│   └── test_agent_evolution.py
└── e2e/
    ├── test_tension_resolution.py
    ├── test_project_lifecycle.py
    └── test_user_scenarios.py
```

#### 8.2. AI-Specific Testing
```python
# Test reasoning quality
async def test_reasoning_agent_quality():
    agent = TensionAnalyzer()
    tension = create_complex_tension()
    
    solutions = await agent.analyze_tension(tension)
    
    # Quality assertions
    assert len(solutions) >= 3
    assert all(s["confidence"] > 0.5 for s in solutions)
    assert solutions[0]["confidence"] > solutions[-1]["confidence"]  # Sorted by confidence

# Test learning capability
async def test_agent_learning():
    agent = TensionAnalyzer()
    
    # Initial performance
    initial_score = await agent.get_performance_score()
    
    # Provide feedback
    await agent.process_feedback({
        "solution_effectiveness": 0.9,
        "user_satisfaction": 0.8,
        "win_impact": {"wisdom": 0.7, "intelligence": 0.8, "networking": 0.6}
    })
    
    # Check improvement
    improved_score = await agent.get_performance_score()
    assert improved_score > initial_score
```

---

## PHẦN IV: MIGRATION TIMELINE

### 9. DETAILED TIMELINE

#### Week 1-2: Core Infrastructure
- [ ] Create trm_core package structure
- [ ] Implement OntologyEntity base class
- [ ] Standardize event schemas
- [ ] Migrate existing ontology definitions
- [ ] Update all imports and references

#### Week 3-4: Agent Ecosystem  
- [ ] Implement BaseAgent pattern
- [ ] Create Genesis Engine MVP
- [ ] Implement first reasoning agents
- [ ] Create agent testing framework
- [ ] Test agent creation and lifecycle

#### Week 5-6: Intelligence Layer
- [ ] Implement TensionAnalyzer
- [ ] Create OutcomeSimulator
- [ ] Add pattern detection capabilities
- [ ] Implement learning mechanisms
- [ ] Test reasoning quality

#### Week 7-8: API v2
- [ ] Design API v2 architecture
- [ ] Implement event-driven endpoints
- [ ] Create WebSocket communication
- [ ] Add real-time monitoring
- [ ] Test API v2 functionality

#### Week 9-10: Integration & Testing
- [ ] End-to-end integration testing
- [ ] Performance optimization
- [ ] Documentation completion
- [ ] Production deployment preparation
- [ ] User acceptance testing

### 10. SUCCESS CRITERIA

#### 10.1. Technical Criteria
- [ ] All existing tests pass (218+ tests)
- [ ] New agent tests achieve >90% coverage
- [ ] Event processing latency <100ms
- [ ] API v2 fully functional
- [ ] Zero regression in v1 API

#### 10.2. Functional Criteria  
- [ ] Genesis Engine can create agents automatically
- [ ] Reasoning agents can analyze tensions effectively
- [ ] Event-driven communication works seamlessly
- [ ] WebSocket real-time updates functional
- [ ] Ontology-first pattern consistently applied

#### 10.3. Quality Criteria
- [ ] Code follows established patterns
- [ ] Documentation is comprehensive
- [ ] Error handling is robust
- [ ] Performance meets requirements
- [ ] Security standards maintained

---

## PHẦN V: RISK MITIGATION

### 11. IDENTIFIED RISKS & MITIGATION

#### 11.1. Technical Risks
**Risk**: Breaking existing functionality during migration
**Mitigation**: 
- Maintain v1 API during transition
- Comprehensive regression testing
- Feature flags for gradual rollout

**Risk**: Agent performance unpredictability
**Mitigation**:
- Circuit breaker patterns
- Performance monitoring
- Manual override capabilities

#### 11.2. Timeline Risks
**Risk**: Underestimating complexity of AI implementation
**Mitigation**:
- Start with MVP versions
- Iterative development approach
- Regular checkpoint reviews

**Risk**: Integration challenges between components
**Mitigation**:
- Early integration testing
- Clear interface contracts
- Modular architecture design

### 12. ROLLBACK PLAN

#### 12.1. Emergency Rollback Procedures
1. **Immediate**: Disable new features via feature flags
2. **Short-term**: Revert to previous stable version
3. **Long-term**: Analyze failures and implement fixes

#### 12.2. Data Protection
- Event sourcing for complete audit trail
- Database snapshots before major changes
- Backup and restore procedures tested

---

**KẾT LUẬN:**

Kế hoạch chuẩn hóa này sẽ biến TRM-OS từ một hệ thống API truyền thống thành một **thực thể AI thông minh** với khả năng tự nhận thức, tự tiến hóa và đồng sáng tạo với con người.

**Nguyên tắc cốt lõi**: Mọi thay đổi phải tuân theo **Ontology-First** và **Event-Driven** patterns để đảm bảo tính nhất quán và khả năng mở rộng.

---

*Tài liệu này sẽ được cập nhật theo tiến trình implementation.* 