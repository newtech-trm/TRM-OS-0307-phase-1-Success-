"""
TRM-OS Agent Ecosystem Manager
=============================

Central management system cho Agent Ecosystem
với intelligent task routing và collaboration coordination
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
import asyncio
import logging
from collections import defaultdict

from trm_api.agents.ecosystem.specialized_agents import (
    SpecializedAgent, AgentSpecialization, AgentCollaborationRequest,
    ProjectManagerAgent, DataAnalystAgent, TensionResolverAgent
)
from trm_api.learning.adaptive_learning_system import AdaptiveLearningSystem
# ML Enhanced Reasoning removed - Using Commercial AI APIs only
from trm_api.reasoning.reasoning_types import ReasoningContext, ReasoningType
from trm_api.quantum.quantum_system_manager import QuantumSystemManager
from trm_api.reasoning.advanced_reasoning_engine import AdvancedReasoningEngine
from trm_api.learning.learning_types import LearningExperience, ExperienceType


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class EcosystemTask:
    """Task trong Agent Ecosystem"""
    task_id: str
    task_type: str
    description: str
    required_specializations: List[AgentSpecialization]
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Assignment tracking
    assigned_agents: List[str] = field(default_factory=list)
    primary_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    
    # Execution tracking
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results
    execution_results: Dict[str, Any] = field(default_factory=dict)
    collaboration_history: List[str] = field(default_factory=list)
    
    # Performance metrics
    estimated_duration: Optional[timedelta] = None
    actual_duration: Optional[timedelta] = None
    success_rate: float = 0.0


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics cho agent"""
    agent_id: str
    specialization: AgentSpecialization
    
    # Task metrics
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_completion_time: float = 0.0
    success_rate: float = 0.0
    
    # Collaboration metrics
    collaborations_initiated: int = 0
    collaborations_received: int = 0
    collaboration_success_rate: float = 0.0
    
    # Quality metrics
    average_confidence_score: float = 0.0
    feedback_score: float = 0.0
    learning_progress: float = 0.0
    
    # Availability
    current_workload: int = 0
    max_concurrent_tasks: int = 5
    availability_score: float = 1.0
    
    last_updated: datetime = field(default_factory=datetime.now)


class AgentEcosystemManager:
    """Central manager cho Agent Ecosystem"""
    
    def __init__(self, system_id: str = None):
        self.system_id = system_id or f"ecosystem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agents: Dict[str, SpecializedAgent] = {}
        self.tasks: Dict[str, EcosystemTask] = {}
        self.performance_metrics: Dict[str, AgentPerformanceMetrics] = {}
        
        # Task routing và scheduling
        self.task_queue: List[str] = []  # Task IDs in priority order
        self.active_tasks: Dict[str, str] = {}  # task_id -> primary_agent_id
        
        # Collaboration tracking
        self.collaboration_requests: Dict[str, AgentCollaborationRequest] = {}
        self.collaboration_networks: Dict[str, List[str]] = defaultdict(list)
        
        # ML components
        self.learning_system = AdaptiveLearningSystem(agent_id=f"ecosystem_manager_{self.system_id}")
        self.quantum_manager = QuantumSystemManager(learning_system=self.learning_system)
        self.advanced_reasoning = AdvancedReasoningEngine(agent_id=f"ecosystem_reasoning_{self.system_id}")
        # ML Enhanced Reasoning removed - Using Commercial AI APIs only
        # Commercial AI coordination per TRM-OS philosophy
        
        # Statistics và monitoring
        self.ecosystem_stats = {
            "total_tasks_processed": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_task_completion_time": 0.0,
            "agent_utilization": 0.0,
            "collaboration_efficiency": 0.0
        }
        
        self.logger = logging.getLogger(f"ecosystem_manager_{self.system_id}")
        self.is_running = False
        
        # Background tasks
        self.background_tasks: List[asyncio.Task] = []
    
    async def initialize(self):
        """Initialize ecosystem manager"""
        try:
            self.logger.info("Initializing Agent Ecosystem Manager...")
            
            # Create default specialized agents
            await self._create_default_agents()
            
            # Start background processes
            await self._start_background_processes()
            
            self.is_running = True
            self.logger.info("Agent Ecosystem Manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ecosystem manager: {e}")
            raise
    
    async def _create_default_agents(self):
        """Create default set of specialized agents"""
        default_agents = [
            ("project_manager_001", ProjectManagerAgent),
            ("data_analyst_001", DataAnalystAgent),
            ("tension_resolver_001", TensionResolverAgent)
        ]
        
        for agent_id, agent_class in default_agents:
            agent = agent_class(agent_id)
            await self.register_agent(agent)
    
    async def register_agent(self, agent: SpecializedAgent):
        """Register new agent trong ecosystem"""
        self.agents[agent.agent_id] = agent
        
        # Initialize performance metrics
        self.performance_metrics[agent.agent_id] = AgentPerformanceMetrics(
            agent_id=agent.agent_id,
            specialization=agent.specialization
        )
        
        self.logger.info(f"Registered agent: {agent.agent_id} ({agent.specialization.value})")
    
    async def submit_task(self, task: EcosystemTask) -> str:
        """Submit task to ecosystem"""
        self.tasks[task.task_id] = task
        
        # Add to priority queue
        await self._add_to_priority_queue(task.task_id)
        
        self.logger.info(f"Task submitted: {task.task_id} ({task.task_type})")
        
        # Trigger task assignment
        asyncio.create_task(self._process_task_queue())
        
        return task.task_id
    
    async def _add_to_priority_queue(self, task_id: str):
        """Add task to priority queue maintaining order"""
        task = self.tasks[task_id]
        
        # Insert based on priority
        inserted = False
        for i, existing_task_id in enumerate(self.task_queue):
            existing_task = self.tasks[existing_task_id]
            if task.priority.value < existing_task.priority.value:
                self.task_queue.insert(i, task_id)
                inserted = True
                break
        
        if not inserted:
            self.task_queue.append(task_id)
    
    async def _process_task_queue(self):
        """Process pending tasks in priority queue"""
        while self.task_queue:
            task_id = self.task_queue[0]
            task = self.tasks[task_id]
            
            if task.status != TaskStatus.PENDING:
                self.task_queue.pop(0)
                continue
            
            # Find best agent for task
            best_agent = await self._find_best_agent_for_task(task)
            
            if best_agent:
                # Assign task
                await self._assign_task_to_agent(task_id, best_agent.agent_id)
                self.task_queue.pop(0)
                
                # Execute task
                asyncio.create_task(self._execute_task(task_id))
            else:
                # No available agent, wait
                break
    
    async def _find_best_agent_for_task(self, task: EcosystemTask) -> Optional[SpecializedAgent]:
        """Find best agent for given task"""
        suitable_agents = []
        
        # Filter agents by specialization
        for agent in self.agents.values():
            if agent.specialization in task.required_specializations:
                metrics = self.performance_metrics[agent.agent_id]
                
                # Check availability
                if metrics.current_workload < metrics.max_concurrent_tasks:
                    suitable_agents.append((agent, metrics))
        
        if not suitable_agents:
            return None
        
        # Score agents using ML reasoning
        try:
            reasoning_context = ReasoningContext(
                context_id=f"task_assignment_{task.task_id}",
                domain="agent_selection",
                constraints={"task_priority": task.priority.value},
                objectives=["optimal_assignment", "load_balancing"],
                available_resources={"agents": len(suitable_agents)},
                priority_level=task.priority.value,
                risk_tolerance=0.5
            )
            
            # Commercial AI coordination would be implemented here
            # For now, use simple scoring without local ML
            
            # Score agents
            agent_scores = []
            for agent, metrics in suitable_agents:
                score = (
                    metrics.success_rate * 0.4 +
                    metrics.availability_score * 0.3 +
                    metrics.average_confidence_score * 0.2 +
                    (1.0 - metrics.current_workload / metrics.max_concurrent_tasks) * 0.1
                )
                
                agent_scores.append((agent, score))
            
            # Return agent with highest score
            best_agent, _ = max(agent_scores, key=lambda x: x[1])
            return best_agent
            
        except Exception as e:
            self.logger.warning(f"Agent selection failed: {e}")
            
            # Fallback to simple scoring
            agent_scores = []
            for agent, metrics in suitable_agents:
                score = metrics.success_rate * (1.0 - metrics.current_workload / metrics.max_concurrent_tasks)
                agent_scores.append((agent, score))
            
            best_agent, _ = max(agent_scores, key=lambda x: x[1])
            return best_agent
    
    async def _assign_task_to_agent(self, task_id: str, agent_id: str):
        """Assign task to specific agent"""
        task = self.tasks[task_id]
        task.primary_agent = agent_id
        task.assigned_agents = [agent_id]
        task.status = TaskStatus.ASSIGNED
        task.assigned_at = datetime.now()
        
        # Update agent workload
        metrics = self.performance_metrics[agent_id]
        metrics.current_workload += 1
        
        # Update active tasks
        self.active_tasks[task_id] = agent_id
        
        self.logger.info(f"Task {task_id} assigned to agent {agent_id}")
    
    async def _execute_task(self, task_id: str):
        """Execute task with assigned agent"""
        task = self.tasks[task_id]
        agent = self.agents[task.primary_agent]
        
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()
            
            # Execute task
            execution_result = await agent.execute_specialized_task({
                "id": task_id,
                "type": task.task_type,
                "description": task.description,
                "priority": task.priority.value,
                "context": task.context
            })
            
            # Update task
            task.execution_results = execution_result
            task.completed_at = datetime.now()
            task.actual_duration = task.completed_at - task.started_at
            
            if execution_result.get("success", False):
                task.status = TaskStatus.COMPLETED
                task.success_rate = execution_result.get("reasoning_confidence", 0.7)
                self.ecosystem_stats["successful_tasks"] += 1
            else:
                task.status = TaskStatus.FAILED
                self.ecosystem_stats["failed_tasks"] += 1
            
            # Update agent metrics
            await self._update_agent_metrics(task.primary_agent, task, execution_result)
            
            # Learn from execution
            await self._learn_from_task_execution(task, execution_result)
            
            # Clean up
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            
            self.ecosystem_stats["total_tasks_processed"] += 1
            
            self.logger.info(f"Task {task_id} completed with status: {task.status.value}")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.execution_results = {"error": str(e)}
            
            self.ecosystem_stats["failed_tasks"] += 1
            self.ecosystem_stats["total_tasks_processed"] += 1
            
            self.logger.error(f"Task {task_id} failed: {e}")
    
    async def _update_agent_metrics(self, agent_id: str, task: EcosystemTask, execution_result: Dict[str, Any]):
        """Update agent performance metrics"""
        metrics = self.performance_metrics[agent_id]
        
        # Update task counts
        if task.status == TaskStatus.COMPLETED:
            metrics.tasks_completed += 1
        else:
            metrics.tasks_failed += 1
        
        # Update success rate
        total_tasks = metrics.tasks_completed + metrics.tasks_failed
        metrics.success_rate = metrics.tasks_completed / total_tasks if total_tasks > 0 else 0.0
        
        # Update completion time
        if task.actual_duration:
            duration_seconds = task.actual_duration.total_seconds()
            metrics.average_completion_time = (
                metrics.average_completion_time * 0.9 + duration_seconds * 0.1
            )
        
        # Update confidence score
        confidence = execution_result.get("reasoning_confidence", 0.5)
        metrics.average_confidence_score = (
            metrics.average_confidence_score * 0.9 + confidence * 0.1
        )
        
        # Update workload
        metrics.current_workload = max(0, metrics.current_workload - 1)
        metrics.availability_score = 1.0 - (metrics.current_workload / metrics.max_concurrent_tasks)
        
        metrics.last_updated = datetime.now()
    
    async def _learn_from_task_execution(self, task: EcosystemTask, execution_result: Dict[str, Any]):
        """Learn from task execution experience"""
        try:
            experience = LearningExperience(
                experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
                agent_id=self.system_id,
                context={
                    "task_type": task.task_type,
                    "specialization_required": [spec.value for spec in task.required_specializations],
                    "priority": task.priority.value,
                    "agent_assigned": task.primary_agent
                },
                action_taken={
                    "task_assignment": True,
                    "agent_selection": task.primary_agent,
                    "collaboration_used": len(task.assigned_agents) > 1
                },
                outcome={
                    "success": task.status == TaskStatus.COMPLETED,
                    "execution_time": task.actual_duration.total_seconds() if task.actual_duration else 0.0,
                    "confidence": execution_result.get("reasoning_confidence", 0.0)
                },
                success=task.status == TaskStatus.COMPLETED,
                confidence_level=execution_result.get("reasoning_confidence", 0.5),
                importance_weight=1.0 / task.priority.value  # Higher priority = higher importance
            )
            
            await self.learning_system.learn_from_experience(experience)
            
        except Exception as e:
            self.logger.error(f"Learning from task execution failed: {e}")
    
    async def _start_background_processes(self):
        """Start background monitoring và optimization processes"""
        self.background_tasks = [
            asyncio.create_task(self._metrics_monitoring_loop()),
            asyncio.create_task(self._load_balancing_loop()),
            asyncio.create_task(self._collaboration_optimization_loop())
        ]
    
    async def _metrics_monitoring_loop(self):
        """Monitor ecosystem metrics"""
        while self.is_running:
            try:
                await self._update_ecosystem_statistics()
                await asyncio.sleep(60)  # Update every minute
            except Exception as e:
                self.logger.error(f"Metrics monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _load_balancing_loop(self):
        """Monitor và balance agent workloads"""
        while self.is_running:
            try:
                await self._balance_agent_workloads()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                self.logger.error(f"Load balancing error: {e}")
                await asyncio.sleep(300)
    
    async def _collaboration_optimization_loop(self):
        """Optimize agent collaborations"""
        while self.is_running:
            try:
                await self._optimize_collaborations()
                await asyncio.sleep(600)  # Check every 10 minutes
            except Exception as e:
                self.logger.error(f"Collaboration optimization error: {e}")
                await asyncio.sleep(600)
    
    async def _update_ecosystem_statistics(self):
        """Update ecosystem-level statistics"""
        if not self.agents:
            return
        
        # Calculate agent utilization
        total_capacity = sum(metrics.max_concurrent_tasks for metrics in self.performance_metrics.values())
        current_load = sum(metrics.current_workload for metrics in self.performance_metrics.values())
        self.ecosystem_stats["agent_utilization"] = current_load / total_capacity if total_capacity > 0 else 0.0
        
        # Calculate average completion time
        completed_tasks = [task for task in self.tasks.values() if task.status == TaskStatus.COMPLETED]
        if completed_tasks:
            avg_time = sum(task.actual_duration.total_seconds() for task in completed_tasks if task.actual_duration) / len(completed_tasks)
            self.ecosystem_stats["average_task_completion_time"] = avg_time
    
    async def _balance_agent_workloads(self):
        """Balance workloads across agents"""
        # Identify overloaded và underloaded agents
        overloaded_agents = []
        underloaded_agents = []
        
        for agent_id, metrics in self.performance_metrics.items():
            utilization = metrics.current_workload / metrics.max_concurrent_tasks
            if utilization > 0.8:  # Over 80% capacity
                overloaded_agents.append(agent_id)
            elif utilization < 0.3:  # Under 30% capacity
                underloaded_agents.append(agent_id)
        
        # Log workload status
        if overloaded_agents or underloaded_agents:
            self.logger.info(f"Load balancing: {len(overloaded_agents)} overloaded, {len(underloaded_agents)} underloaded agents")
    
    async def _optimize_collaborations(self):
        """Optimize agent collaboration patterns"""
        # Analyze collaboration success rates
        successful_collaborations = 0
        total_collaborations = len(self.collaboration_requests)
        
        for request in self.collaboration_requests.values():
            # Simple success metric based on request completion
            if hasattr(request, 'completed') and request.completed:
                successful_collaborations += 1
        
        if total_collaborations > 0:
            self.ecosystem_stats["collaboration_efficiency"] = successful_collaborations / total_collaborations
    
    def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get comprehensive ecosystem status"""
        return {
            "system_id": self.system_id,
            "is_running": self.is_running,
            "agents": {
                agent_id: agent.get_agent_status()
                for agent_id, agent in self.agents.items()
            },
            "tasks": {
                "total": len(self.tasks),
                "pending": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
                "in_progress": len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
                "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
                "failed": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
            },
            "performance_metrics": {
                agent_id: {
                    "success_rate": metrics.success_rate,
                    "current_workload": metrics.current_workload,
                    "availability_score": metrics.availability_score
                }
                for agent_id, metrics in self.performance_metrics.items()
            },
            "ecosystem_stats": self.ecosystem_stats,
            "queue_length": len(self.task_queue),
            "active_tasks": len(self.active_tasks)
        }
    
    async def shutdown(self):
        """Shutdown ecosystem manager"""
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if self.background_tasks:
            await asyncio.gather(*self.background_tasks, return_exceptions=True)
        
        self.logger.info("Agent Ecosystem Manager shutdown complete") 