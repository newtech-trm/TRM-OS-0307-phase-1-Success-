"""
Causal Analyzer - Component for causal relationship analysis

Provides sophisticated causal analysis capabilities for the Advanced Reasoning Engine
following TRM-OS ontology principles.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from .reasoning_types import CausalChain, ReasoningContext, UncertaintyLevel


class CausalAnalyzer:
    """
    Analyzes causal relationships between events, entities, and states
    
    Core capabilities:
    1. Event sequence analysis to identify causal patterns
    2. Entity relationship causal mapping
    3. Temporal causal inference
    4. Causal strength estimation
    5. Multi-level causal chain discovery
    """
    
    def __init__(self):
        self.logger = logging.getLogger("reasoning.causal_analyzer")
        
        # Causal pattern templates based on TRM-OS ontology
        self.ontology_causal_patterns = {
            "tension_to_task": {
                "cause_type": "tension",
                "effect_type": "task", 
                "relationship": "creates",
                "strength_base": 0.8,
                "confidence_base": 0.9
            },
            "task_to_event": {
                "cause_type": "task",
                "effect_type": "event",
                "relationship": "triggers",
                "strength_base": 0.9,
                "confidence_base": 0.95
            },
            "event_to_win": {
                "cause_type": "event", 
                "effect_type": "win",
                "relationship": "leads_to",
                "strength_base": 0.7,
                "confidence_base": 0.8
            },
            "agent_to_event": {
                "cause_type": "agent",
                "effect_type": "event",
                "relationship": "actor_triggered",
                "strength_base": 0.85,
                "confidence_base": 0.9
            }
        }
        
        # Temporal thresholds for causal inference
        self.temporal_thresholds = {
            "immediate": timedelta(minutes=5),     # Very likely causal
            "short_term": timedelta(hours=2),      # Likely causal
            "medium_term": timedelta(hours=24),    # Possibly causal
            "long_term": timedelta(days=7)         # Unlikely causal
        }
    
    async def analyze_relationships(
        self, 
        entities: List[str], 
        context: ReasoningContext
    ) -> List[CausalChain]:
        """
        Analyze causal relationships between entities
        
        Args:
            entities: List of entity identifiers to analyze
            context: Reasoning context with historical data
            
        Returns:
            List of discovered causal chains
        """
        self.logger.info(f"Analyzing causal relationships for {len(entities)} entities")
        
        causal_chains = []
        
        try:
            # Analyze pairwise relationships
            for i, entity1 in enumerate(entities):
                for entity2 in entities[i+1:]:
                    chains = await self._analyze_entity_pair(entity1, entity2, context)
                    causal_chains.extend(chains)
            
            # Analyze multi-entity chains
            if len(entities) > 2:
                multi_chains = await self._analyze_multi_entity_chains(entities, context)
                causal_chains.extend(multi_chains)
            
            # Filter and rank chains by strength and confidence
            causal_chains = self._filter_and_rank_chains(causal_chains)
            
            self.logger.info(f"Found {len(causal_chains)} causal relationships")
            
        except Exception as e:
            self.logger.error(f"Error in causal analysis: {str(e)}")
        
        return causal_chains
    
    async def analyze_event_sequences(
        self, 
        events: List[Dict[str, Any]]
    ) -> List[CausalChain]:
        """
        Analyze causal relationships in event sequences
        
        Args:
            events: List of historical events with timestamps
            
        Returns:
            List of causal chains discovered in event sequences
        """
        # Handle None input
        if events is None:
            events = []
            
        self.logger.info(f"Analyzing causal patterns in {len(events)} events")
        
        if not events or len(events) < 2:
            return []
        
        causal_chains = []
        
        try:
            # Sort events by timestamp
            sorted_events = sorted(
                events, 
                key=lambda e: e.get("timestamp", datetime.min)
            )
            
            # Analyze sequential patterns
            for i, event1 in enumerate(sorted_events[:-1]):
                for j in range(i+1, min(i+5, len(sorted_events))):  # Look ahead max 4 events
                    event2 = sorted_events[j]
                    
                    chain = await self._analyze_event_pair(event1, event2)
                    if chain and chain.confidence >= 0.5:
                        causal_chains.append(chain)
            
            # Look for longer causal sequences
            sequence_chains = await self._find_causal_sequences(sorted_events)
            causal_chains.extend(sequence_chains)
            
            # Remove duplicates and weak relationships
            causal_chains = self._deduplicate_chains(causal_chains)
            
            self.logger.info(f"Found {len(causal_chains)} causal chains in events")
            
        except Exception as e:
            self.logger.error(f"Error analyzing event sequences: {str(e)}")
        
        return causal_chains
    
    async def _analyze_entity_pair(
        self, 
        entity1: str, 
        entity2: str, 
        context: ReasoningContext
    ) -> List[CausalChain]:
        """Analyze causal relationship between two entities"""
        
        chains = []
        
        # Extract entity types
        type1 = self._extract_entity_type(entity1)
        type2 = self._extract_entity_type(entity2)
        
        # Check for known ontology patterns
        pattern_key = f"{type1}_to_{type2}"
        reverse_pattern_key = f"{type2}_to_{type1}"
        
        if pattern_key in self.ontology_causal_patterns:
            chain = await self._create_ontology_chain(
                entity1, entity2, 
                self.ontology_causal_patterns[pattern_key],
                context
            )
            if chain:
                chains.append(chain)
        
        elif reverse_pattern_key in self.ontology_causal_patterns:
            chain = await self._create_ontology_chain(
                entity2, entity1,
                self.ontology_causal_patterns[reverse_pattern_key], 
                context
            )
            if chain:
                chains.append(chain)
        
        # Analyze temporal relationships from historical events
        temporal_chain = await self._analyze_temporal_causality(entity1, entity2, context)
        if temporal_chain:
            chains.append(temporal_chain)
        
        return chains
    
    async def _analyze_multi_entity_chains(
        self, 
        entities: List[str], 
        context: ReasoningContext
    ) -> List[CausalChain]:
        """Analyze causal chains involving multiple entities"""
        
        chains = []
        
        # Look for 3-entity chains following Recognition → Event → WIN pattern
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities):
                if i == j:
                    continue
                for k, entity3 in enumerate(entities):
                    if k == i or k == j:
                        continue
                    
                    # Check if this forms a valid causal sequence
                    chain = await self._check_three_entity_chain(
                        entity1, entity2, entity3, context
                    )
                    if chain:
                        chains.append(chain)
        
        return chains
    
    async def _analyze_event_pair(
        self, 
        event1: Dict[str, Any], 
        event2: Dict[str, Any]
    ) -> Optional[CausalChain]:
        """Analyze causal relationship between two events"""
        
        # Calculate temporal distance
        time1 = event1.get("timestamp")
        time2 = event2.get("timestamp")
        
        if not time1 or not time2:
            return None
        
        time_diff = time2 - time1
        
        # Events must be in correct temporal order
        if time_diff.total_seconds() <= 0:
            return None
        
        # Determine causal likelihood based on temporal proximity
        causal_likelihood = self._calculate_temporal_causal_likelihood(time_diff)
        
        if causal_likelihood < 0.3:  # Too weak to consider
            return None
        
        # Extract event information
        event1_type = event1.get("event_type", "unknown")
        event2_type = event2.get("event_type", "unknown")
        event1_id = event1.get("event_id", "unknown")
        event2_id = event2.get("event_id", "unknown")
        
        # Check for semantic relationships
        semantic_strength = self._calculate_semantic_causal_strength(event1, event2)
        
        # Create causal chain
        chain = CausalChain(
            root_cause=f"event_{event1_type}_{event1_id}",
            final_effect=f"event_{event2_type}_{event2_id}",
            confidence=causal_likelihood * semantic_strength,
            strength=semantic_strength,
            evidence=[
                {
                    "type": "temporal",
                    "time_difference_seconds": time_diff.total_seconds(),
                    "causal_likelihood": causal_likelihood
                },
                {
                    "type": "semantic", 
                    "event1_type": event1_type,
                    "event2_type": event2_type,
                    "semantic_strength": semantic_strength
                }
            ],
            relationships=[(event1_id, event2_id, semantic_strength)]
        )
        
        return chain
    
    async def _find_causal_sequences(
        self, 
        events: List[Dict[str, Any]]
    ) -> List[CausalChain]:
        """Find longer causal sequences in events"""
        
        sequences = []
        
        # Group events by type to find patterns
        event_groups = defaultdict(list)
        for event in events:
            event_type = event.get("event_type", "unknown")
            event_groups[event_type].append(event)
        
        # Look for recurring patterns that might indicate causal sequences
        for event_type, type_events in event_groups.items():
            if len(type_events) >= 3:
                # Analyze intervals between events of same type
                intervals = []
                for i in range(len(type_events) - 1):
                    time_diff = (
                        type_events[i+1].get("timestamp", datetime.min) - 
                        type_events[i].get("timestamp", datetime.min)
                    )
                    intervals.append(time_diff.total_seconds())
                
                # If intervals are consistent, might indicate causal pattern
                if intervals and self._is_consistent_pattern(intervals):
                    chain = CausalChain(
                        root_cause=f"pattern_{event_type}_recurring",
                        final_effect=f"sequence_{event_type}_pattern",
                        confidence=0.6,
                        strength=0.7,
                        evidence=[{
                            "type": "recurring_pattern",
                            "event_type": event_type,
                            "occurrences": len(type_events),
                            "avg_interval_seconds": sum(intervals) / len(intervals)
                        }]
                    )
                    sequences.append(chain)
        
        return sequences
    
    async def _create_ontology_chain(
        self, 
        cause_entity: str, 
        effect_entity: str,
        pattern: Dict[str, Any], 
        context: ReasoningContext
    ) -> Optional[CausalChain]:
        """Create causal chain based on ontology pattern"""
        
        # Adjust confidence based on context
        context_adjustment = self._calculate_context_adjustment(
            cause_entity, effect_entity, context
        )
        
        confidence = pattern["confidence_base"] * context_adjustment
        strength = pattern["strength_base"] * context_adjustment
        
        if confidence < 0.4:  # Too weak
            return None
        
        chain = CausalChain(
            root_cause=cause_entity,
            final_effect=effect_entity,
            confidence=confidence,
            strength=strength,
            evidence=[
                {
                    "type": "ontology_pattern",
                    "pattern_type": f"{pattern['cause_type']}_to_{pattern['effect_type']}",
                    "relationship": pattern["relationship"],
                    "context_adjustment": context_adjustment
                }
            ],
            relationships=[(cause_entity, effect_entity, strength)]
        )
        
        return chain
    
    async def _analyze_temporal_causality(
        self, 
        entity1: str, 
        entity2: str, 
        context: ReasoningContext
    ) -> Optional[CausalChain]:
        """Analyze temporal causality between entities based on historical events"""
        
        # Find events related to both entities
        entity1_events = []
        entity2_events = []
        
        for event in context.historical_events:
            event_data = event.get("data", {})
            entity_id = event.get("entity_id")
            
            if entity_id == entity1 or entity1 in str(event_data):
                entity1_events.append(event)
            
            if entity_id == entity2 or entity2 in str(event_data):
                entity2_events.append(event)
        
        if not entity1_events or not entity2_events:
            return None
        
        # Find temporal patterns
        causal_evidence = []
        total_strength = 0
        count = 0
        
        for e1 in entity1_events:
            for e2 in entity2_events:
                time1 = e1.get("timestamp")
                time2 = e2.get("timestamp")
                
                if time1 and time2 and time2 > time1:
                    time_diff = time2 - time1
                    likelihood = self._calculate_temporal_causal_likelihood(time_diff)
                    
                    if likelihood > 0.3:
                        causal_evidence.append({
                            "event1": e1.get("event_id"),
                            "event2": e2.get("event_id"),
                            "time_diff_seconds": time_diff.total_seconds(),
                            "likelihood": likelihood
                        })
                        total_strength += likelihood
                        count += 1
        
        if count == 0:
            return None
        
        avg_strength = total_strength / count
        confidence = min(0.9, avg_strength * (count / max(len(entity1_events), len(entity2_events))))
        
        chain = CausalChain(
            root_cause=entity1,
            final_effect=entity2,
            confidence=confidence,
            strength=avg_strength,
            evidence=[{
                "type": "temporal_analysis",
                "causal_instances": count,
                "avg_strength": avg_strength,
                "evidence_details": causal_evidence
            }],
            relationships=[(entity1, entity2, avg_strength)]
        )
        
        return chain
    
    async def _check_three_entity_chain(
        self, 
        entity1: str, 
        entity2: str, 
        entity3: str,
        context: ReasoningContext
    ) -> Optional[CausalChain]:
        """Check if three entities form a valid causal chain"""
        
        # Check for Recognition → Event → WIN pattern
        type1 = self._extract_entity_type(entity1)
        type2 = self._extract_entity_type(entity2)  
        type3 = self._extract_entity_type(entity3)
        
        # Look for pattern: tension → task → event or agent → event → win
        valid_patterns = [
            ("tension", "task", "event"),
            ("agent", "event", "win"),
            ("task", "event", "win"),
            ("tension", "event", "task")
        ]
        
        pattern_match = (type1, type2, type3) in valid_patterns
        
        if not pattern_match:
            return None
        
        # Verify temporal ordering if available
        temporal_score = await self._verify_temporal_ordering(
            [entity1, entity2, entity3], context
        )
        
        if temporal_score < 0.4:
            return None
        
        chain = CausalChain(
            root_cause=entity1,
            intermediate_causes=[entity2],
            final_effect=entity3,
            confidence=0.7 * temporal_score,
            strength=0.8,
            evidence=[
                {
                    "type": "three_entity_pattern",
                    "pattern": f"{type1} → {type2} → {type3}",
                    "temporal_score": temporal_score
                }
            ],
            relationships=[
                (entity1, entity2, 0.8),
                (entity2, entity3, 0.8)
            ]
        )
        
        return chain
    
    def _extract_entity_type(self, entity: str) -> str:
        """Extract entity type from entity identifier"""
        
        if entity.startswith("tension_"):
            return "tension"
        elif entity.startswith("task_"):
            return "task"
        elif entity.startswith("agent_"):
            return "agent"
        elif entity.startswith("event_"):
            return "event"
        elif entity.startswith("win_"):
            return "win"
        elif entity.startswith("project_"):
            return "project"
        else:
            return "unknown"
    
    def _calculate_temporal_causal_likelihood(self, time_diff: timedelta) -> float:
        """Calculate causal likelihood based on temporal distance"""
        
        if time_diff <= self.temporal_thresholds["immediate"]:
            return 0.9
        elif time_diff <= self.temporal_thresholds["short_term"]:
            return 0.7
        elif time_diff <= self.temporal_thresholds["medium_term"]:
            return 0.5
        elif time_diff <= self.temporal_thresholds["long_term"]:
            return 0.3
        else:
            return 0.1
    
    def _calculate_semantic_causal_strength(
        self, 
        event1: Dict[str, Any], 
        event2: Dict[str, Any]
    ) -> float:
        """Calculate semantic causal strength between events"""
        
        type1 = event1.get("event_type", "")
        type2 = event2.get("event_type", "")
        
        # Known causal relationships between event types
        causal_pairs = {
            ("TENSION_CREATED", "TASK_CREATED"): 0.8,
            ("TASK_CREATED", "TASK_UPDATED"): 0.7,
            ("TASK_UPDATED", "TASK_COMPLETED"): 0.9,
            ("TASK_COMPLETED", "TENSION_RESOLVED"): 0.8,
            ("AGENT_ACTIVATED", "TASK_CREATED"): 0.6,
            ("KNOWLEDGE_CREATED", "TASK_UPDATED"): 0.5
        }
        
        # Check direct relationships
        if (type1, type2) in causal_pairs:
            return causal_pairs[(type1, type2)]
        
        # Check for similar event types
        if type1 == type2:
            return 0.4  # Same type events have moderate causal strength
        
        # Check for related entities
        entity1 = event1.get("entity_id")
        entity2 = event2.get("entity_id")
        
        if entity1 and entity2 and entity1 == entity2:
            return 0.6  # Same entity increases causal strength
        
        return 0.3  # Default weak relationship
    
    def _calculate_context_adjustment(
        self, 
        cause_entity: str, 
        effect_entity: str, 
        context: ReasoningContext
    ) -> float:
        """Calculate context-based adjustment for causal relationships"""
        
        adjustment = 1.0
        
        # Adjust based on priority level
        if context.priority_level >= 8:
            adjustment *= 1.1  # High priority increases confidence
        elif context.priority_level <= 3:
            adjustment *= 0.9  # Low priority decreases confidence
        
        # Adjust based on complexity
        if context.complexity_score >= 0.8:
            adjustment *= 0.9  # High complexity decreases confidence
        elif context.complexity_score <= 0.3:
            adjustment *= 1.1  # Low complexity increases confidence
        
        # Adjust based on data availability
        if len(context.historical_events) >= 20:
            adjustment *= 1.05  # More data increases confidence
        elif len(context.historical_events) <= 5:
            adjustment *= 0.95  # Less data decreases confidence
        
        return min(1.2, max(0.7, adjustment))  # Clamp between 0.7 and 1.2
    
    def _is_consistent_pattern(self, intervals: List[float]) -> bool:
        """Check if time intervals show consistent pattern"""
        
        if len(intervals) < 3:
            return False
        
        # Calculate coefficient of variation
        mean_interval = sum(intervals) / len(intervals)
        variance = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        if mean_interval == 0:
            return False
        
        cv = std_dev / mean_interval
        
        # Consider pattern consistent if CV < 0.5
        return cv < 0.5
    
    async def _verify_temporal_ordering(
        self, 
        entities: List[str], 
        context: ReasoningContext
    ) -> float:
        """Verify temporal ordering of entities based on historical events"""
        
        entity_timestamps = {}
        
        # Find first occurrence timestamp for each entity
        for entity in entities:
            for event in context.historical_events:
                entity_id = event.get("entity_id")
                event_data = event.get("data", {})
                
                if entity_id == entity or entity in str(event_data):
                    if entity not in entity_timestamps:
                        entity_timestamps[entity] = event.get("timestamp")
                    else:
                        # Keep earliest timestamp
                        current_time = entity_timestamps[entity]
                        event_time = event.get("timestamp")
                        if event_time and (not current_time or event_time < current_time):
                            entity_timestamps[entity] = event_time
        
        # Check if entities appear in expected order
        valid_orderings = 0
        total_pairs = 0
        
        for i in range(len(entities) - 1):
            entity1 = entities[i]
            entity2 = entities[i + 1]
            
            time1 = entity_timestamps.get(entity1)
            time2 = entity_timestamps.get(entity2)
            
            if time1 and time2:
                total_pairs += 1
                if time1 <= time2:
                    valid_orderings += 1
        
        if total_pairs == 0:
            return 0.5  # No temporal data available
        
        return valid_orderings / total_pairs
    
    def _filter_and_rank_chains(self, chains: List[CausalChain]) -> List[CausalChain]:
        """Filter and rank causal chains by quality"""
        
        # Filter chains with minimum confidence threshold
        filtered_chains = [
            chain for chain in chains 
            if chain.confidence >= 0.4 and chain.strength >= 0.3
        ]
        
        # Rank by combined confidence and strength
        filtered_chains.sort(
            key=lambda c: c.confidence * c.strength, 
            reverse=True
        )
        
        # Keep top 20 chains to avoid information overload
        return filtered_chains[:20]
    
    def _deduplicate_chains(self, chains: List[CausalChain]) -> List[CausalChain]:
        """Remove duplicate causal chains"""
        
        seen_relationships = set()
        unique_chains = []
        
        for chain in chains:
            # Create signature based on cause and effect
            signature = (chain.root_cause, chain.final_effect)
            
            if signature not in seen_relationships:
                seen_relationships.add(signature)
                unique_chains.append(chain)
            else:
                # If duplicate, keep the one with higher confidence
                for i, existing_chain in enumerate(unique_chains):
                    if (existing_chain.root_cause == chain.root_cause and 
                        existing_chain.final_effect == chain.final_effect):
                        
                        if chain.confidence > existing_chain.confidence:
                            unique_chains[i] = chain
                        break 