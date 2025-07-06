"""
Context Manager - Component for managing and enriching reasoning context

Provides context enrichment capabilities using TRM-OS ontology data
for the Advanced Reasoning Engine.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from .reasoning_types import ReasoningContext


class ContextManager:
    """
    Manages and enriches reasoning context with ontology data
    
    Core capabilities:
    1. Context enrichment with related ontology entities
    2. Historical data aggregation and analysis
    3. Entity relationship mapping
    4. Temporal context establishment
    5. Context quality assessment
    """
    
    def __init__(self):
        self.logger = logging.getLogger("reasoning.context_manager")
        
        # Context enrichment settings
        self.max_historical_events = 100
        self.max_related_entities = 50
        self.default_time_window_days = 30
    
    async def enrich_context(self, context: ReasoningContext) -> ReasoningContext:
        """
        Enrich reasoning context with relevant ontology data
        
        Args:
            context: Basic reasoning context to enrich
            
        Returns:
            Enriched context with additional ontology information
        """
        self.logger.info(f"Enriching context {context.context_id}")
        
        enriched_context = context.copy(deep=True)
        
        try:
            # For initial implementation, perform basic enrichment
            await self._basic_enrichment(enriched_context)
            
            # Establish temporal context
            await self._establish_temporal_context(enriched_context)
            
            # Assess context quality
            context_quality = await self._assess_context_quality(enriched_context)
            enriched_context.current_state["context_quality"] = context_quality
            
            self.logger.info(
                f"Context enrichment complete: "
                f"{len(enriched_context.related_entities)} entity types, "
                f"{len(enriched_context.historical_events)} events"
            )
            
        except Exception as e:
            self.logger.error(f"Error enriching context: {str(e)}")
            # Return original context if enrichment fails
            return context
        
        return enriched_context
    
    async def _basic_enrichment(self, context: ReasoningContext) -> None:
        """Perform basic context enrichment without external dependencies"""
        
        # Enrich tension data if available
        if context.tension_id:
            context.current_state.update({
                "tension_status": "open",
                "tension_priority": context.priority_level
            })
            
            if "tension" not in context.related_entities:
                context.related_entities["tension"] = []
            context.related_entities["tension"].append(context.tension_id)
        
        # Enrich task data if available
        if context.task_ids:
            for task_id in context.task_ids:
                context.current_state.update({
                    f"task_{task_id}_status": "in_progress",
                    f"task_{task_id}_priority": 5
                })
            
            if "task" not in context.related_entities:
                context.related_entities["task"] = []
            context.related_entities["task"].extend(context.task_ids)
        
        # Enrich agent data if available
        if context.agent_id:
            context.current_state.update({
                "agent_status": "active",
                "agent_type": "reasoning_agent"
            })
            
            if "agent" not in context.related_entities:
                context.related_entities["agent"] = []
            context.related_entities["agent"].append(context.agent_id)
    
    async def _establish_temporal_context(self, context: ReasoningContext) -> None:
        """Establish temporal context and patterns"""
        
        try:
            if not context.historical_events:
                # Set default time window
                now = datetime.now()
                context.time_window = (
                    now - timedelta(days=self.default_time_window_days),
                    now
                )
                return
            
            # Analyze temporal patterns
            event_timestamps = [
                event.get("timestamp") for event in context.historical_events
                if event.get("timestamp")
            ]
            
            if event_timestamps:
                earliest = min(event_timestamps)
                latest = max(event_timestamps)
                
                # Calculate time span
                time_span = latest - earliest
                context.current_state["analysis_time_span_days"] = time_span.days
                
                # Calculate event frequency
                if time_span.total_seconds() > 0:
                    events_per_day = len(event_timestamps) / max(1, time_span.days)
                    context.current_state["event_frequency_per_day"] = events_per_day
                
                # Identify recent activity burst
                recent_threshold = latest - timedelta(days=1)
                recent_events = [ts for ts in event_timestamps if ts > recent_threshold]
                
                if len(recent_events) > len(event_timestamps) * 0.3:
                    context.current_state["recent_activity_burst"] = True
                    context.priority_level = min(10, context.priority_level + 1)
            
        except Exception as e:
            self.logger.error(f"Error establishing temporal context: {str(e)}")
    
    async def _assess_context_quality(self, context: ReasoningContext) -> Dict[str, Any]:
        """Assess the quality and completeness of the context"""
        
        quality_assessment = {
            "overall_score": 0.0,
            "completeness": 0.0,
            "freshness": 0.0,
            "entity_coverage": 0.0,
            "temporal_coverage": 0.0
        }
        
        try:
            # Assess completeness
            completeness_factors = []
            
            if context.tension_id:
                completeness_factors.append(0.3)
            if context.task_ids:
                completeness_factors.append(0.2)
            if context.agent_id:
                completeness_factors.append(0.15)
            if context.project_id:
                completeness_factors.append(0.15)
            if context.historical_events:
                completeness_factors.append(0.2)
            
            quality_assessment["completeness"] = sum(completeness_factors)
            
            # Assess freshness
            if context.historical_events:
                now = datetime.now()
                recent_threshold = now - timedelta(hours=24)
                
                recent_events = [
                    event for event in context.historical_events
                    if event.get("timestamp", datetime.min) > recent_threshold
                ]
                
                freshness_ratio = len(recent_events) / len(context.historical_events)
                quality_assessment["freshness"] = freshness_ratio
            else:
                quality_assessment["freshness"] = 0.0
            
            # Assess entity coverage
            entity_types = len(context.related_entities.keys())
            
            if entity_types >= 4:
                entity_coverage = 1.0
            elif entity_types >= 3:
                entity_coverage = 0.8
            elif entity_types >= 2:
                entity_coverage = 0.6
            else:
                entity_coverage = 0.3
                
            quality_assessment["entity_coverage"] = entity_coverage
            
            # Assess temporal coverage
            if context.time_window:
                time_span = context.time_window[1] - context.time_window[0]
                span_days = time_span.days
                
                if span_days >= 30:
                    temporal_coverage = 1.0
                elif span_days >= 14:
                    temporal_coverage = 0.8
                elif span_days >= 7:
                    temporal_coverage = 0.6
                else:
                    temporal_coverage = 0.4
                    
                quality_assessment["temporal_coverage"] = temporal_coverage
            else:
                quality_assessment["temporal_coverage"] = 0.0
            
            # Calculate overall score
            weights = {
                "completeness": 0.3,
                "freshness": 0.2,
                "entity_coverage": 0.3,
                "temporal_coverage": 0.2
            }
            
            overall_score = sum(
                quality_assessment[factor] * weight
                for factor, weight in weights.items()
            )
            
            quality_assessment["overall_score"] = overall_score
            
        except Exception as e:
            self.logger.error(f"Error assessing context quality: {str(e)}")
        
        return quality_assessment 