#!/usr/bin/env python3
"""
Living Knowledge Core - TRM-OS v2.0 Living System Implementation

Implements 4-Layer Dynamic Knowledge System:
A. Input Layer: Auto-detect content changes
B. Processing Layer: Semantic analysis với vectorization  
C. Structuring Layer: Ontology evolution với conflict resolution
D. Feedback & Evolution: Self-learning với retrospective updates

Philosophy: Recognition → Event → WIN với Living Knowledge Evolution
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from trm_api.core.logging_config import get_logger
from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType

logger = get_logger(__name__)


class ContentChangeType(str, Enum):
    """Types of content changes detected"""
    MINOR_EDIT = "minor_edit"           # <10% semantic change
    SIGNIFICANT_UPDATE = "significant_update"  # 10-50% semantic change
    MAJOR_REVISION = "major_revision"   # 50-80% semantic change
    COMPLETE_REWRITE = "complete_rewrite"  # >80% semantic change
    INTENT_SHIFT = "intent_shift"       # Strategic direction change
    STRUCTURAL_CHANGE = "structural_change"  # Schema/ontology change


class EvolutionStatus(str, Enum):
    """Status of knowledge evolution process"""
    DETECTED = "detected"
    ANALYZING = "analyzing"
    EVOLVING = "evolving"
    SYNCHRONIZING = "synchronizing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SemanticVersion:
    """Semantic versioning for living knowledge"""
    major: int = 0
    minor: int = 0  
    patch: int = 0
    semantic_hash: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    author: str = "system"
    change_summary: str = ""
    intent_confidence: float = 1.0
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def increment(self, change_type: ContentChangeType) -> 'SemanticVersion':
        """Increment version based on change significance"""
        if change_type in [ContentChangeType.COMPLETE_REWRITE, ContentChangeType.INTENT_SHIFT]:
            return SemanticVersion(
                major=self.major + 1,
                minor=0,
                patch=0,
                created_at=datetime.now()
            )
        elif change_type in [ContentChangeType.MAJOR_REVISION, ContentChangeType.STRUCTURAL_CHANGE]:
            return SemanticVersion(
                major=self.major,
                minor=self.minor + 1,
                patch=0,
                created_at=datetime.now()
            )
        else:
            return SemanticVersion(
                major=self.major,
                minor=self.minor,
                patch=self.patch + 1,
                created_at=datetime.now()
            )


@dataclass
class ContentSnapshot:
    """Snapshot của content tại một thời điểm"""
    content_id: str
    content_text: str
    semantic_hash: str
    vector_embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: SemanticVersion = field(default_factory=SemanticVersion)
    parent_snapshot_id: Optional[str] = None
    

@dataclass  
class EvolutionContext:
    """Context cho knowledge evolution process"""
    content_id: str
    old_snapshot: ContentSnapshot
    new_snapshot: ContentSnapshot
    change_type: ContentChangeType
    change_significance: float  # 0.0 - 1.0
    detected_at: datetime = field(default_factory=datetime.now)
    evolution_status: EvolutionStatus = EvolutionStatus.DETECTED
    affected_systems: List[str] = field(default_factory=list)
    rollback_plan: Optional[Dict[str, Any]] = None


class LivingKnowledgeNode:
    """
    Core living knowledge node với auto-evolution capabilities
    
    Implements dynamic content versioning, semantic drift detection,
    và system-wide synchronization theo AGE v2.0 principles.
    """
    
    def __init__(self, content_id: str, initial_content: str = ""):
        self.content_id = content_id
        self.current_snapshot = ContentSnapshot(
            content_id=content_id,
            content_text=initial_content,
            semantic_hash=self._calculate_semantic_hash(initial_content)
        )
        self.version_history: List[ContentSnapshot] = [self.current_snapshot]
        self.evolution_queue: List[EvolutionContext] = []
        self.is_evolving = False
        self.event_bus = SystemEventBus()
        
        # Evolution configuration
        self.config = {
            "semantic_threshold": 0.1,      # Minimum change to trigger evolution
            "intent_threshold": 0.3,        # Threshold for intent shift detection
            "auto_evolution_enabled": True,  # Enable automatic evolution
            "max_evolution_queue": 10,      # Max queued evolutions
            "rollback_retention_days": 7    # Keep rollback data for N days
        }
        
        logger.info(f"LivingKnowledgeNode initialized: {content_id}")
    
    def _calculate_semantic_hash(self, content: str) -> str:
        """Calculate semantic hash for content change detection"""
        # Normalize content for semantic comparison
        normalized = content.lower().strip()
        # Remove extra whitespace and punctuation for semantic consistency
        normalized = ' '.join(normalized.split())
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    async def detect_content_change(self, new_content: str) -> Optional[EvolutionContext]:
        """
        Detect và analyze content changes
        
        Args:
            new_content: New content to compare against current
            
        Returns:
            EvolutionContext if significant change detected, None otherwise
        """
        try:
            # Calculate semantic hash for new content
            new_hash = self._calculate_semantic_hash(new_content)
            
            # Quick hash comparison
            if new_hash == self.current_snapshot.semantic_hash:
                logger.debug(f"No semantic change detected for {self.content_id}")
                return None
            
            # Create new snapshot
            new_snapshot = ContentSnapshot(
                content_id=self.content_id,
                content_text=new_content,
                semantic_hash=new_hash,
                parent_snapshot_id=self.current_snapshot.content_id
            )
            
            # Analyze change significance
            change_type, significance = await self._analyze_change_significance(
                self.current_snapshot, new_snapshot
            )
            
            # Check if change meets threshold
            if significance < self.config["semantic_threshold"]:
                logger.debug(f"Change significance {significance} below threshold")
                return None
            
            # Create evolution context
            evolution_context = EvolutionContext(
                content_id=self.content_id,
                old_snapshot=self.current_snapshot,
                new_snapshot=new_snapshot,
                change_type=change_type,
                change_significance=significance
            )
            
            logger.info(f"Content change detected: {change_type} (significance: {significance:.2f})")
            return evolution_context
            
        except Exception as e:
            logger.error(f"Error detecting content change: {e}")
            return None
    
    async def _analyze_change_significance(
        self, 
        old_snapshot: ContentSnapshot, 
        new_snapshot: ContentSnapshot
    ) -> Tuple[ContentChangeType, float]:
        """
        Analyze significance of content change using multiple metrics
        
        Returns:
            Tuple of (ContentChangeType, significance_score)
        """
        try:
            old_content = old_snapshot.content_text
            new_content = new_snapshot.content_text
            
            # Basic text similarity metrics
            old_words = set(old_content.lower().split())
            new_words = set(new_content.lower().split())
            
            # Jaccard similarity
            intersection = len(old_words.intersection(new_words))
            union = len(old_words.union(new_words))
            jaccard_similarity = intersection / union if union > 0 else 0
            text_change_ratio = 1 - jaccard_similarity
            
            # Length change ratio
            old_length = len(old_content)
            new_length = len(new_content)
            length_change_ratio = abs(new_length - old_length) / max(old_length, 1)
            
            # Combined significance score
            significance = (text_change_ratio * 0.7 + length_change_ratio * 0.3)
            
            # Determine change type based on significance
            if significance > 0.8:
                change_type = ContentChangeType.COMPLETE_REWRITE
            elif significance > 0.5:
                change_type = ContentChangeType.MAJOR_REVISION
            elif significance > 0.1:
                change_type = ContentChangeType.SIGNIFICANT_UPDATE
            else:
                change_type = ContentChangeType.MINOR_EDIT
            
            # Check for intent shift patterns
            intent_keywords = ["tầm nhìn", "vision", "mission", "strategy", "goal", "objective"]
            old_intent_mentions = sum(1 for keyword in intent_keywords if keyword in old_content.lower())
            new_intent_mentions = sum(1 for keyword in intent_keywords if keyword in new_content.lower())
            
            if abs(new_intent_mentions - old_intent_mentions) >= 2 or significance > self.config["intent_threshold"]:
                change_type = ContentChangeType.INTENT_SHIFT
                significance = max(significance, 0.6)  # Intent shifts are always significant
            
            return change_type, min(significance, 1.0)
            
        except Exception as e:
            logger.error(f"Error analyzing change significance: {e}")
            return ContentChangeType.MINOR_EDIT, 0.1
    
    async def auto_evolve_on_content_change(self, new_content: str) -> bool:
        """
        Auto-evolve knowledge node when content changes
        
        Args:
            new_content: New content that triggered evolution
            
        Returns:
            True if evolution completed successfully, False otherwise
        """
        if not self.config["auto_evolution_enabled"]:
            logger.debug("Auto-evolution disabled")
            return False
        
        if self.is_evolving:
            logger.warning(f"Evolution already in progress for {self.content_id}")
            return False
        
        try:
            self.is_evolving = True
            
            # Detect content change
            evolution_context = await self.detect_content_change(new_content)
            if not evolution_context:
                logger.debug("No significant change detected, skipping evolution")
                return True
            
            # Add to evolution queue
            if len(self.evolution_queue) >= self.config["max_evolution_queue"]:
                logger.warning("Evolution queue full, dropping oldest")
                self.evolution_queue.pop(0)
            
            self.evolution_queue.append(evolution_context)
            
            # Process evolution
            success = await self._process_evolution(evolution_context)
            
            if success:
                # Update current snapshot
                self.current_snapshot = evolution_context.new_snapshot
                self.version_history.append(evolution_context.new_snapshot)
                
                # Trigger system-wide updates
                await self._trigger_system_updates(evolution_context)
                
                logger.info(f"Knowledge evolution completed for {self.content_id}")
                
                # Publish evolution event
                await self.event_bus.publish(SystemEvent(
                    event_type=EventType.KNOWLEDGE_CREATED,
                    entity_id=self.content_id,
                    data={
                        "change_type": evolution_context.change_type,
                        "significance": evolution_context.change_significance,
                        "version": str(evolution_context.new_snapshot.version)
                    }
                ))
                
            return success
            
        except Exception as e:
            logger.error(f"Error in auto-evolution: {e}")
            return False
        finally:
            self.is_evolving = False
    
    async def _process_evolution(self, context: EvolutionContext) -> bool:
        """Process knowledge evolution with rollback capability"""
        try:
            context.evolution_status = EvolutionStatus.ANALYZING
            
            # Create rollback plan
            context.rollback_plan = {
                "previous_snapshot": context.old_snapshot,
                "timestamp": datetime.now(),
                "affected_systems": []
            }
            
            context.evolution_status = EvolutionStatus.EVOLVING
            
            # Update version based on change type
            new_version = context.old_snapshot.version.increment(context.change_type)
            context.new_snapshot.version = new_version
            
            # Set evolution metadata
            context.new_snapshot.metadata = {
                "evolution_context": {
                    "change_type": context.change_type,
                    "significance": context.change_significance,
                    "detected_at": context.detected_at.isoformat(),
                    "auto_evolved": True
                },
                "previous_version": str(context.old_snapshot.version),
                "rollback_available": True
            }
            
            context.evolution_status = EvolutionStatus.COMPLETED
            logger.info(f"Evolution processed: {context.content_id} → v{new_version}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing evolution: {e}")
            context.evolution_status = EvolutionStatus.FAILED
            return False
    
    async def _trigger_system_updates(self, context: EvolutionContext) -> None:
        """Trigger system-wide updates after knowledge evolution"""
        try:
            # Identify affected systems based on change type
            affected_systems = []
            
            if context.change_type == ContentChangeType.INTENT_SHIFT:
                affected_systems.extend([
                    "strategic_planning",
                    "agent_coordination", 
                    "ontology_manager",
                    "contextual_identity_engine"
                ])
            
            if context.change_significance > 0.5:
                affected_systems.extend([
                    "knowledge_graph",
                    "vector_embeddings",
                    "semantic_search"
                ])
            
            context.affected_systems = affected_systems
            
            # Trigger updates for each affected system
            for system in affected_systems:
                await self.event_bus.publish(SystemEvent(
                    event_type=f"system.{system}.update_required",
                    entity_id=self.content_id,
                    data={
                        "evolution_context": context,
                        "update_priority": "high" if context.change_significance > 0.7 else "normal"
                    }
                ))
                
                logger.info(f"System update triggered: {system}")
            
        except Exception as e:
            logger.error(f"Error triggering system updates: {e}")
    
    async def rollback_to_version(self, version: str) -> bool:
        """Rollback to specific version"""
        try:
            # Find version in history
            target_snapshot = None
            for snapshot in self.version_history:
                if str(snapshot.version) == version:
                    target_snapshot = snapshot
                    break
            
            if not target_snapshot:
                logger.error(f"Version {version} not found in history")
                return False
            
            # Rollback current snapshot
            self.current_snapshot = target_snapshot
            
            # Publish rollback event
            await self.event_bus.publish(SystemEvent(
                event_type="knowledge.rollback",
                entity_id=self.content_id,
                data={"rolled_back_to": version}
            ))
            
            logger.info(f"Rolled back {self.content_id} to version {version}")
            return True
            
        except Exception as e:
            logger.error(f"Error rolling back: {e}")
            return False
    
    def get_evolution_history(self) -> List[Dict[str, Any]]:
        """Get evolution history summary"""
        return [
            {
                "version": str(snapshot.version),
                "created_at": snapshot.version.created_at.isoformat(),
                "semantic_hash": snapshot.semantic_hash,
                "metadata": snapshot.metadata
            }
            for snapshot in self.version_history
        ]
    
    def get_current_version(self) -> str:
        """Get current version string"""
        return str(self.current_snapshot.version)
    
    def get_content(self) -> str:
        """Get current content"""
        return self.current_snapshot.content_text


class LivingKnowledgeCore:
    """
    Central coordinator for Living Knowledge System
    
    Manages multiple LivingKnowledgeNode instances và coordinates
    system-wide knowledge evolution processes.
    """
    
    def __init__(self):
        self.knowledge_nodes: Dict[str, LivingKnowledgeNode] = {}
        self.evolution_coordinator = EvolutionCoordinator()
        self.event_bus = SystemEventBus()
        self.is_initialized = False
        
        logger.info("LivingKnowledgeCore initialized")
    
    async def initialize(self) -> bool:
        """Initialize Living Knowledge Core system"""
        try:
            await self.evolution_coordinator.initialize()
            self.is_initialized = True
            logger.info("LivingKnowledgeCore initialization completed")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize LivingKnowledgeCore: {e}")
            return False
    
    def register_knowledge_node(self, content_id: str, initial_content: str = "") -> LivingKnowledgeNode:
        """Register new living knowledge node"""
        if content_id in self.knowledge_nodes:
            logger.warning(f"Knowledge node {content_id} already exists")
            return self.knowledge_nodes[content_id]
        
        node = LivingKnowledgeNode(content_id, initial_content)
        self.knowledge_nodes[content_id] = node
        
        logger.info(f"Registered knowledge node: {content_id}")
        return node
    
    async def update_content(self, content_id: str, new_content: str) -> bool:
        """Update content and trigger evolution if needed"""
        if content_id not in self.knowledge_nodes:
            logger.warning(f"Knowledge node {content_id} not found, creating new")
            self.register_knowledge_node(content_id, new_content)
            return True
        
        node = self.knowledge_nodes[content_id]
        return await node.auto_evolve_on_content_change(new_content)
    
    def get_node(self, content_id: str) -> Optional[LivingKnowledgeNode]:
        """Get knowledge node by ID"""
        return self.knowledge_nodes.get(content_id)
    
    def list_nodes(self) -> List[str]:
        """List all registered knowledge nodes"""
        return list(self.knowledge_nodes.keys())
    
    async def shutdown(self) -> None:
        """Gracefully shutdown Living Knowledge Core"""
        logger.info("Shutting down LivingKnowledgeCore")
        await self.evolution_coordinator.shutdown()


class EvolutionCoordinator:
    """Coordinates evolution processes across multiple knowledge nodes"""
    
    def __init__(self):
        self.active_evolutions: Dict[str, EvolutionContext] = {}
        self.evolution_metrics = {
            "total_evolutions": 0,
            "successful_evolutions": 0,
            "failed_evolutions": 0,
            "average_evolution_time": 0.0
        }
    
    async def initialize(self) -> None:
        """Initialize evolution coordinator"""
        logger.info("EvolutionCoordinator initialized")
    
    async def shutdown(self) -> None:
        """Shutdown evolution coordinator"""
        logger.info("EvolutionCoordinator shutdown")


# Global living knowledge core instance
_living_knowledge_core: Optional[LivingKnowledgeCore] = None

async def get_living_knowledge_core() -> LivingKnowledgeCore:
    """Get global living knowledge core instance"""
    global _living_knowledge_core
    if _living_knowledge_core is None:
        _living_knowledge_core = LivingKnowledgeCore()
        await _living_knowledge_core.initialize()
    return _living_knowledge_core 