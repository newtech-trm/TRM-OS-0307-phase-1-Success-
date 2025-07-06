"""
Experience Collector for Adaptive Learning System

Collects and stores learning experiences from agent actions and outcomes.
Follows TRM-OS philosophy: Recognition → Event → WIN through experience capture.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from uuid import uuid4

from .learning_types import (
    LearningExperience, 
    ExperienceType, 
    MetricType,
    LearningSession,
    safe_enum_value
)
from ..eventbus.system_event_bus import publish_event, EventType


class ExperienceCollector:
    """Collects and manages learning experiences for agents"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"learning.experience_collector.{agent_id}")
        
        # Experience storage
        self.experiences: Dict[str, LearningExperience] = {}
        self.active_sessions: Dict[str, LearningSession] = {}
        
        # Collection statistics
        self.collection_stats = {
            "total_experiences": 0,
            "experiences_by_type": {},
            "avg_confidence": 0.0,
            "avg_importance": 0.0,
            "collection_rate": 0.0  # experiences per hour
        }
        
        # Configuration
        self.auto_capture_enabled = True
        self.min_confidence_threshold = 0.3
        self.max_experiences_stored = 10000  # Memory management
        
    async def start_learning_session(
        self, 
        session_type: str = "general",
        goals: List[str] = None
    ) -> str:
        """Start a new learning session"""
        
        session = LearningSession(
            agent_id=self.agent_id,
            session_type=session_type,
            goals=goals or []
        )
        
        self.active_sessions[session.session_id] = session
        
        self.logger.info(f"Started learning session {session.session_id} of type {session_type}")
        
        # Create learning session event
        await publish_event(
            event_type=EventType.AGENT_ACTION_COMPLETED,
            source_agent_id=self.agent_id,
            entity_id=session.session_id,
            entity_type="learning_session",
            data={
                "action": "learning_session_started",
                "session_type": session_type,
                "goals": goals or []
            }
        )
        
        return session.session_id
    
    async def collect_task_experience(
        self,
        task_id: str,
        action_taken: Dict[str, Any],
        outcome: Dict[str, Any],
        success: bool,
        performance_before: Dict[str, float] = None,
        performance_after: Dict[str, float] = None,
        context: Dict[str, Any] = None,
        session_id: Optional[str] = None
    ) -> str:
        """Collect experience from task execution"""
        
        experience = LearningExperience(
            experience_type=ExperienceType.PERFORMANCE_OPTIMIZATION,
            agent_id=self.agent_id,
            task_id=task_id,
            action_taken=action_taken,
            outcome=outcome,
            success=success,
            performance_before=performance_before or {},
            performance_after=performance_after or {},
            context=context or {}
        )
        
        # Calculate improvement
        if performance_before and performance_after:
            experience.improvement = self._calculate_improvement(
                performance_before, performance_after
            )
        
        return await self._store_experience(experience, session_id)
    
    async def collect_problem_solving_experience(
        self,
        problem_description: str,
        solution_approach: Dict[str, Any],
        outcome: Dict[str, Any],
        success: bool,
        confidence_level: float = 0.5,
        context: Dict[str, Any] = None,
        session_id: Optional[str] = None
    ) -> str:
        """Collect experience from problem solving"""
        
        experience = LearningExperience(
            experience_type=ExperienceType.TENSION_RESOLUTION,
            agent_id=self.agent_id,
            action_taken={
                "problem": problem_description,
                "approach": solution_approach
            },
            outcome=outcome,
            success=success,
            confidence_level=confidence_level,
            context=context or {}
        )
        
        return await self._store_experience(experience, session_id)
    
    async def collect_decision_experience(
        self,
        decision_context: Dict[str, Any],
        options_considered: List[Dict[str, Any]],
        decision_made: Dict[str, Any],
        outcome: Dict[str, Any],
        success: bool,
        confidence_level: float = 0.5,
        session_id: Optional[str] = None
    ) -> str:
        """Collect experience from decision making"""
        
        experience = LearningExperience(
            experience_type=ExperienceType.BEHAVIORAL_ADAPTATION,
            agent_id=self.agent_id,
            action_taken={
                "options_considered": options_considered,
                "decision_made": decision_made
            },
            outcome=outcome,
            success=success,
            confidence_level=confidence_level,
            context=decision_context
        )
        
        return await self._store_experience(experience, session_id)
    
    async def collect_interaction_experience(
        self,
        interaction_type: str,
        other_agent_id: str,
        interaction_data: Dict[str, Any],
        outcome: Dict[str, Any],
        success: bool,
        context: Dict[str, Any] = None,
        session_id: Optional[str] = None
    ) -> str:
        """Collect experience from agent interactions"""
        
        experience = LearningExperience(
            experience_type=ExperienceType.FEEDBACK_PROCESSING,
            agent_id=self.agent_id,
            action_taken={
                "interaction_type": interaction_type,
                "other_agent": other_agent_id,
                "interaction_data": interaction_data
            },
            outcome=outcome,
            success=success,
            context=context or {}
        )
        
        return await self._store_experience(experience, session_id)
    
    async def collect_error_recovery_experience(
        self,
        error_type: str,
        error_details: Dict[str, Any],
        recovery_actions: List[Dict[str, Any]],
        recovery_success: bool,
        context: Dict[str, Any] = None,
        session_id: Optional[str] = None
    ) -> str:
        """Collect experience from error recovery"""
        
        experience = LearningExperience(
            experience_type=ExperienceType.PATTERN_RECOGNITION,
            agent_id=self.agent_id,
            action_taken={
                "error_type": error_type,
                "error_details": error_details,
                "recovery_actions": recovery_actions
            },
            outcome={"recovery_success": recovery_success},
            success=recovery_success,
            context=context or {}
        )
        
        return await self._store_experience(experience, session_id)
    
    async def finalize_learning_session(
        self, 
        session_id: str,
        performance_after: Dict[str, float] = None,
        success: bool = True
    ) -> LearningSession:
        """Finalize a learning session"""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"No active session found with ID {session_id}")
        
        session = self.active_sessions[session_id]
        
        if performance_after:
            session.performance_after = performance_after
        
        session.finalize_session(success)
        
        # Move from active to completed
        completed_session = self.active_sessions.pop(session_id)
        
        self.logger.info(
            f"Finalized learning session {session_id} with "
            f"{len(session.experiences)} experiences collected"
        )
        
        # Create session completion event
        await publish_event(
            event_type=EventType.AGENT_ACTION_COMPLETED,
            source_agent_id=self.agent_id,
            entity_id=session_id,
            entity_type="learning_session",
            data={
                "action": "learning_session_completed",
                "success": success,
                "experiences_collected": len(session.experiences),
                "duration_seconds": session.duration_seconds,
                "learning_effectiveness": session.learning_effectiveness
            }
        )
        
        return completed_session
    
    async def _store_experience(
        self, 
        experience: LearningExperience,
        session_id: Optional[str] = None
    ) -> str:
        """Store experience and update statistics"""
        
        # Validate experience quality
        if experience.confidence_level < self.min_confidence_threshold:
            self.logger.warning(
                f"Experience {experience.experience_id} has low confidence "
                f"({experience.confidence_level}), storing anyway"
            )
        
        # Store experience
        self.experiences[experience.experience_id] = experience
        
        # Add to active session if specified
        if session_id and session_id in self.active_sessions:
            self.active_sessions[session_id].experiences.append(experience.experience_id)
        
        # Update statistics
        self._update_collection_stats(experience)
        
        # Memory management
        await self._manage_memory()
        
        self.logger.debug(
            f"Stored experience {experience.experience_id} of type "
            f"{safe_enum_value(experience.experience_type)}"
        )
        
        # Create experience collection event
        await publish_event(
            event_type=EventType.KNOWLEDGE_CREATED,
            source_agent_id=self.agent_id,
            entity_id=experience.experience_id,
            entity_type="learning_experience",
            data={
                "experience_type": safe_enum_value(experience.experience_type),
                "success": experience.success,
                "confidence": experience.confidence_level,
                "importance": experience.importance_weight
            }
        )
        
        return experience.experience_id
    
    def _calculate_improvement(
        self, 
        before: Dict[str, float], 
        after: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate performance improvement"""
        
        improvement = {}
        
        for metric in before:
            if metric in after:
                before_val = before[metric]
                after_val = after[metric]
                
                if before_val != 0:
                    improvement[metric] = (after_val - before_val) / abs(before_val)
                else:
                    improvement[metric] = after_val
        
        return improvement
    
    def _update_collection_stats(self, experience: LearningExperience) -> None:
        """Update collection statistics"""
        
        self.collection_stats["total_experiences"] += 1
        
        # Update by type - handle both enum and string values
        exp_type = experience.experience_type
        if hasattr(exp_type, 'value'):
            exp_type = safe_enum_value(exp_type)
        else:
            exp_type = str(exp_type)
            
        if exp_type not in self.collection_stats["experiences_by_type"]:
            self.collection_stats["experiences_by_type"][exp_type] = 0
        self.collection_stats["experiences_by_type"][exp_type] += 1
        
        # Update averages
        total = self.collection_stats["total_experiences"]
        current_avg_conf = self.collection_stats["avg_confidence"]
        current_avg_imp = self.collection_stats["avg_importance"]
        
        self.collection_stats["avg_confidence"] = (
            (current_avg_conf * (total - 1) + experience.confidence_level) / total
        )
        
        self.collection_stats["avg_importance"] = (
            (current_avg_imp * (total - 1) + experience.importance_weight) / total
        )
    
    async def _manage_memory(self) -> None:
        """Manage memory by removing old experiences if needed"""
        
        if len(self.experiences) > self.max_experiences_stored:
            # Remove oldest experiences (simple FIFO strategy)
            experiences_to_remove = len(self.experiences) - self.max_experiences_stored
            
            # Sort by timestamp and remove oldest
            sorted_experiences = sorted(
                self.experiences.items(),
                key=lambda x: x[1].timestamp
            )
            
            for i in range(experiences_to_remove):
                exp_id = sorted_experiences[i][0]
                del self.experiences[exp_id]
                
            self.logger.info(f"Removed {experiences_to_remove} old experiences for memory management")
    
    def get_experiences_by_type(self, experience_type: ExperienceType) -> List[LearningExperience]:
        """Get experiences filtered by type"""
        return [
            exp for exp in self.experiences.values()
            if exp.experience_type == experience_type
        ]
    
    def get_experiences_by_success(self, success: bool) -> List[LearningExperience]:
        """Get experiences filtered by success status"""
        return [
            exp for exp in self.experiences.values()
            if exp.success == success
        ]
    
    def get_recent_experiences(self, hours: int = 24) -> List[LearningExperience]:
        """Get experiences from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [
            exp for exp in self.experiences.values()
            if exp.timestamp >= cutoff_time
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get collection statistics"""
        return self.collection_stats.copy()
    
    def clear_experiences(self) -> None:
        """Clear all stored experiences (use with caution)"""
        self.experiences.clear()
        self.collection_stats = {
            "total_experiences": 0,
            "experiences_by_type": {},
            "avg_confidence": 0.0,
            "avg_importance": 0.0,
            "collection_rate": 0.0
        }
        self.logger.info("Cleared all stored experiences") 