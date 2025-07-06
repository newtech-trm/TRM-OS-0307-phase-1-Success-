"""
ReasoningService - Integration layer for TRM-OS Reasoning Engine

Integrates reasoning engine with:
- Existing tension services
- Project and agent repositories
- Event bus system
- Notification services
"""

from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..reasoning import (
    ReasoningCoordinator,
    ReasoningRequest,
    ReasoningResult
)
from ..repositories.tension_repository import TensionRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.agent_repository import AgentRepository
from ..eventbus.system_event_bus import SystemEventBus
from ..models.tension import Tension
from ..models.enums import TensionStatus, Priority
from ..core.config import get_settings

class ReasoningService:
    """
    Service layer for integrating reasoning engine with TRM-OS ecosystem.
    
    Provides:
    - Automated tension analysis on creation/update
    - Integration with existing repositories
    - Event-driven reasoning triggers
    - Notification and escalation handling
    """
    
    def __init__(self, 
                 tension_repository: TensionRepository,
                 project_repository: ProjectRepository,
                 agent_repository: AgentRepository,
                 event_bus: SystemEventBus):
        self.logger = logging.getLogger(__name__)
        
        # Repositories
        self.tension_repo = tension_repository
        self.project_repo = project_repository
        self.agent_repo = agent_repository
        
        # Event bus
        self.event_bus = event_bus
        
        # Reasoning engine
        self.reasoning_coordinator = ReasoningCoordinator()
        
        # Configuration
        self.settings = get_settings()
        
        # Register event handlers
        self._register_event_handlers()
    
    def _register_event_handlers(self):
        """Register event handlers for automatic reasoning triggers"""
        
        # Tension created/updated events
        self.event_bus.subscribe("tension.created", self._handle_tension_created)
        self.event_bus.subscribe("tension.updated", self._handle_tension_updated)
        
        # Project events
        self.event_bus.subscribe("project.created", self._handle_project_created)
        
        # Agent events
        self.event_bus.subscribe("agent.assigned", self._handle_agent_assigned)
    
    async def analyze_tension_automatically(self, tension_id: str) -> Optional[ReasoningResult]:
        """
        Automatically analyze tension and apply results
        
        Args:
            tension_id: ID of tension to analyze
            
        Returns:
            ReasoningResult if successful, None if failed
        """
        try:
            self.logger.info(f"Starting automatic analysis for tension {tension_id}")
            
            # Get tension from database
            tension = await self.tension_repo.get_by_id(tension_id)
            if not tension:
                self.logger.error(f"Tension {tension_id} not found")
                return None
            
            # Get additional context
            context = await self._build_tension_context(tension)
            
            # Create reasoning request
            reasoning_request = ReasoningRequest(
                tension_id=tension_id,
                title=tension.title,
                description=tension.description or "",
                current_status=tension.status,
                context=context
            )
            
            # Process through reasoning engine
            result = await self.reasoning_coordinator.process_tension(reasoning_request)
            
            if result.success:
                # Apply reasoning results to tension
                await self._apply_reasoning_results(tension, result)
                
                # Publish reasoning completed event
                await self.event_bus.publish("reasoning.completed", {
                    "tension_id": tension_id,
                    "analysis_type": "automatic",
                    "success": True,
                    "processing_time": result.processing_time,
                    "recommendations_count": len(result.recommendations)
                })
                
                self.logger.info(f"Automatic analysis completed for tension {tension_id}")
            else:
                self.logger.error(f"Reasoning failed for tension {tension_id}: {result.errors}")
                
                # Publish failure event
                await self.event_bus.publish("reasoning.failed", {
                    "tension_id": tension_id,
                    "errors": result.errors
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Automatic analysis failed for tension {tension_id}: {str(e)}")
            return None
    
    async def _build_tension_context(self, tension: Tension) -> Dict[str, Any]:
        """Build comprehensive context for tension analysis"""
        context = {}
        
        try:
            # Project context
            if tension.project_id:
                project = await self.project_repo.get_by_id(tension.project_id)
                if project:
                    context["project"] = {
                        "name": project.name,
                        "description": project.description,
                        "status": project.status,
                        "created_at": project.created_at.isoformat() if project.created_at else None
                    }
            
            # Tension metadata
            context["tension_metadata"] = {
                "created_at": tension.created_at.isoformat() if tension.created_at else None,
                "updated_at": tension.updated_at.isoformat() if tension.updated_at else None,
                "priority": tension.priority,
                "status": tension.status
            }
            
            # Related tensions (simplified - could be enhanced with actual relationships)
            related_tensions = await self.tension_repo.get_by_project_id(tension.project_id) if tension.project_id else []
            context["related_tensions_count"] = len([t for t in related_tensions if t.id != tension.id])
            
            # Time-based context
            if tension.created_at:
                age_days = (datetime.now() - tension.created_at).days
                context["age_days"] = age_days
                
                if age_days > 30:
                    context["stale_tension"] = True
                elif age_days < 1:
                    context["new_tension"] = True
            
            # Priority context
            if tension.priority == Priority.HIGH.value:
                context["high_priority"] = True
            elif tension.priority == Priority.CRITICAL.value:
                context["critical_priority"] = True
            
            # Status context
            if tension.status == TensionStatus.OPEN.value:
                context["open_status"] = True
            elif tension.status == TensionStatus.IN_PROGRESS.value:
                context["in_progress"] = True
            
        except Exception as e:
            self.logger.warning(f"Failed to build complete context for tension {tension.id}: {str(e)}")
        
        return context
    
    async def _apply_reasoning_results(self, tension: Tension, result: ReasoningResult):
        """Apply reasoning results to tension and related entities"""
        
        try:
            updates = {}
            
            # Apply priority calculation results
            if result.priority_calculation:
                new_priority = result.priority_calculation.normalized_priority
                
                # Map to TRM-OS priority values
                priority_mapping = {0: Priority.NORMAL.value, 1: Priority.HIGH.value, 2: Priority.CRITICAL.value}
                mapped_priority = priority_mapping.get(new_priority, tension.priority)
                
                if mapped_priority != tension.priority:
                    updates["priority"] = mapped_priority
                    
                    self.logger.info(f"Updated tension {tension.id} priority: {tension.priority} -> {mapped_priority}")
            
            # Apply analysis results (could add tags, categories, etc.)
            if result.analysis:
                # Could add analysis metadata to tension
                analysis_metadata = {
                    "ai_analysis": {
                        "tension_type": result.analysis.tension_type.value,
                        "confidence": result.analysis.confidence_score,
                        "themes": result.analysis.key_themes,
                        "analyzed_at": datetime.now().isoformat()
                    }
                }
                
                # Store in tension metadata or description
                if tension.description:
                    # Could append analysis summary to description
                    pass
            
            # Apply rule results
            if result.rule_results:
                triggered_rules = [r for r in result.rule_results if r.get("matched", False)]
                if triggered_rules:
                    self.logger.info(f"Triggered {len(triggered_rules)} rules for tension {tension.id}")
                    
                    # Handle specific rule actions
                    for rule_result in triggered_rules:
                        await self._handle_rule_actions(tension, rule_result)
            
            # Update tension if there are changes
            if updates:
                await self.tension_repo.update(tension.id, updates)
                
                # Publish tension updated event
                await self.event_bus.publish("tension.ai_updated", {
                    "tension_id": tension.id,
                    "updates": updates,
                    "reasoning_result": "applied"
                })
            
            # Store solutions as recommendations (could be in separate table)
            if result.solutions:
                await self._store_solution_recommendations(tension.id, result.solutions)
            
        except Exception as e:
            self.logger.error(f"Failed to apply reasoning results for tension {tension.id}: {str(e)}")
    
    async def _handle_rule_actions(self, tension: Tension, rule_result: Dict[str, Any]):
        """Handle specific rule actions"""
        
        try:
            rule_name = rule_result.get("rule_name", "")
            actions = rule_result.get("action_results", [])
            
            for action in actions:
                action_type = action.get("action_type", "")
                parameters = action.get("parameters", {})
                
                if action_type == "escalate_tension":
                    await self._escalate_tension(tension, parameters)
                elif action_type == "assign_security_team":
                    await self._assign_security_team(tension, parameters)
                elif action_type == "notify_business_stakeholders":
                    await self._notify_business_stakeholders(tension, parameters)
                elif action_type == "add_tag":
                    await self._add_tension_tag(tension, parameters.get("tag", ""))
                elif action_type == "assign_to_team":
                    await self._assign_to_team(tension, parameters.get("team", ""))
                else:
                    self.logger.info(f"Unhandled rule action: {action_type} for tension {tension.id}")
            
        except Exception as e:
            self.logger.error(f"Failed to handle rule actions for tension {tension.id}: {str(e)}")
    
    async def _escalate_tension(self, tension: Tension, parameters: Dict[str, Any]):
        """Escalate tension based on rule parameters"""
        
        escalation_level = parameters.get("escalation_level", "normal")
        notify_stakeholders = parameters.get("notify_stakeholders", False)
        create_incident = parameters.get("create_incident", False)
        
        self.logger.info(f"Escalating tension {tension.id} to {escalation_level} level")
        
        # Update priority to critical if not already
        if tension.priority != Priority.CRITICAL.value:
            await self.tension_repo.update(tension.id, {"priority": Priority.CRITICAL.value})
        
        # Publish escalation event
        await self.event_bus.publish("tension.escalated", {
            "tension_id": tension.id,
            "escalation_level": escalation_level,
            "notify_stakeholders": notify_stakeholders,
            "create_incident": create_incident,
            "escalated_by": "reasoning_engine"
        })
    
    async def _assign_security_team(self, tension: Tension, parameters: Dict[str, Any]):
        """Assign tension to security team"""
        
        team = parameters.get("team", "security")
        sla = parameters.get("sla", "4_hours")
        
        self.logger.info(f"Assigning tension {tension.id} to {team} team with {sla} SLA")
        
        # Publish team assignment event
        await self.event_bus.publish("tension.team_assigned", {
            "tension_id": tension.id,
            "team": team,
            "sla": sla,
            "assigned_by": "reasoning_engine"
        })
    
    async def _notify_business_stakeholders(self, tension: Tension, parameters: Dict[str, Any]):
        """Notify business stakeholders"""
        
        stakeholder_groups = parameters.get("stakeholder_groups", [])
        
        self.logger.info(f"Notifying stakeholders for tension {tension.id}: {stakeholder_groups}")
        
        # Publish notification event
        await self.event_bus.publish("stakeholders.notify", {
            "tension_id": tension.id,
            "stakeholder_groups": stakeholder_groups,
            "notification_type": "business_impact",
            "triggered_by": "reasoning_engine"
        })
    
    async def _add_tension_tag(self, tension: Tension, tag: str):
        """Add tag to tension"""
        
        self.logger.info(f"Adding tag '{tag}' to tension {tension.id}")
        
        # Publish tag event (could be handled by tag service)
        await self.event_bus.publish("tension.tag_added", {
            "tension_id": tension.id,
            "tag": tag,
            "added_by": "reasoning_engine"
        })
    
    async def _assign_to_team(self, tension: Tension, team: str):
        """Assign tension to specific team"""
        
        self.logger.info(f"Assigning tension {tension.id} to {team} team")
        
        # Publish team assignment event
        await self.event_bus.publish("tension.team_assigned", {
            "tension_id": tension.id,
            "team": team,
            "assigned_by": "reasoning_engine"
        })
    
    async def _store_solution_recommendations(self, tension_id: str, solutions: List):
        """Store solution recommendations for tension"""
        
        try:
            # Could store in separate recommendations table
            # For now, just publish event
            
            solution_summaries = []
            for solution in solutions:
                summary = {
                    "id": solution.id,
                    "title": solution.title,
                    "type": solution.solution_type.value,
                    "priority": solution.priority.name,
                    "confidence": solution.confidence_score
                }
                solution_summaries.append(summary)
            
            await self.event_bus.publish("solutions.generated", {
                "tension_id": tension_id,
                "solutions": solution_summaries,
                "generated_by": "reasoning_engine"
            })
            
            self.logger.info(f"Stored {len(solutions)} solution recommendations for tension {tension_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to store solutions for tension {tension_id}: {str(e)}")
    
    # Event handlers
    async def _handle_tension_created(self, event_data: Dict[str, Any]):
        """Handle tension created event"""
        
        tension_id = event_data.get("tension_id")
        if tension_id:
            self.logger.info(f"Tension created event received: {tension_id}")
            
            # Trigger automatic analysis (could be async background task)
            # For now, just log - actual implementation would use background tasks
            self.logger.info(f"Scheduling automatic analysis for new tension {tension_id}")
    
    async def _handle_tension_updated(self, event_data: Dict[str, Any]):
        """Handle tension updated event"""
        
        tension_id = event_data.get("tension_id")
        changes = event_data.get("changes", {})
        
        if tension_id and changes:
            self.logger.info(f"Tension updated event received: {tension_id} with changes: {list(changes.keys())}")
            
            # Re-analyze if significant changes
            significant_fields = ["title", "description", "priority"]
            if any(field in changes for field in significant_fields):
                self.logger.info(f"Significant changes detected, scheduling re-analysis for tension {tension_id}")
    
    async def _handle_project_created(self, event_data: Dict[str, Any]):
        """Handle project created event"""
        
        project_id = event_data.get("project_id")
        if project_id:
            self.logger.info(f"Project created event received: {project_id}")
            
            # Could trigger project-level analysis or setup
            pass
    
    async def _handle_agent_assigned(self, event_data: Dict[str, Any]):
        """Handle agent assigned event"""
        
        tension_id = event_data.get("tension_id")
        agent_id = event_data.get("agent_id")
        
        if tension_id and agent_id:
            self.logger.info(f"Agent {agent_id} assigned to tension {tension_id}")
            
            # Could trigger agent-specific analysis or recommendations
            pass
    
    # Public API methods
    async def get_tension_insights(self, tension_id: str) -> Optional[Dict[str, Any]]:
        """Get AI insights for specific tension"""
        
        try:
            # Get tension
            tension = await self.tension_repo.get_by_id(tension_id)
            if not tension:
                return None
            
            # Get context and analyze
            context = await self._build_tension_context(tension)
            
            reasoning_request = ReasoningRequest(
                tension_id=tension_id,
                title=tension.title,
                description=tension.description or "",
                current_status=tension.status,
                context=context,
                requested_services=["analysis", "priority"]  # Lightweight analysis
            )
            
            result = await self.reasoning_coordinator.process_tension(reasoning_request)
            
            if result.success:
                insights = {
                    "tension_id": tension_id,
                    "analysis": {
                        "type": result.analysis.tension_type.value if result.analysis else "Unknown",
                        "confidence": result.analysis.confidence_score if result.analysis else 0,
                        "themes": result.analysis.key_themes if result.analysis else [],
                        "priority_suggestion": result.analysis.suggested_priority if result.analysis else 0
                    },
                    "priority_score": result.priority_calculation.final_score if result.priority_calculation else 0,
                    "recommendations": result.recommendations,
                    "generated_at": datetime.now().isoformat()
                }
                
                return insights
            else:
                return {"error": "Analysis failed", "errors": result.errors}
                
        except Exception as e:
            self.logger.error(f"Failed to get insights for tension {tension_id}: {str(e)}")
            return {"error": str(e)}
    
    async def get_project_reasoning_summary(self, project_id: str) -> Dict[str, Any]:
        """Get reasoning summary for all tensions in project"""
        
        try:
            # Get all tensions for project
            tensions = await self.tension_repo.get_by_project_id(project_id)
            
            summary = {
                "project_id": project_id,
                "total_tensions": len(tensions),
                "analysis_summary": {
                    "types": {},
                    "priorities": {"critical": 0, "high": 0, "normal": 0},
                    "themes": {}
                },
                "recommendations": [],
                "generated_at": datetime.now().isoformat()
            }
            
            # Analyze each tension (simplified)
            for tension in tensions[:10]:  # Limit to avoid performance issues
                insights = await self.get_tension_insights(tension.id)
                if insights and "analysis" in insights:
                    analysis = insights["analysis"]
                    
                    # Count types
                    tension_type = analysis.get("type", "Unknown")
                    summary["analysis_summary"]["types"][tension_type] = summary["analysis_summary"]["types"].get(tension_type, 0) + 1
                    
                    # Count themes
                    for theme in analysis.get("themes", []):
                        summary["analysis_summary"]["themes"][theme] = summary["analysis_summary"]["themes"].get(theme, 0) + 1
                    
                    # Count priorities
                    priority_suggestion = analysis.get("priority_suggestion", 0)
                    if priority_suggestion == 2:
                        summary["analysis_summary"]["priorities"]["critical"] += 1
                    elif priority_suggestion == 1:
                        summary["analysis_summary"]["priorities"]["high"] += 1
                    else:
                        summary["analysis_summary"]["priorities"]["normal"] += 1
            
            # Generate project-level recommendations
            if summary["analysis_summary"]["priorities"]["critical"] > 0:
                summary["recommendations"].append("🚨 Critical tensions require immediate attention")
            
            if summary["analysis_summary"]["themes"].get("Security", 0) > 0:
                summary["recommendations"].append("🔐 Security review recommended for project")
            
            if summary["analysis_summary"]["themes"].get("Technology", 0) > 2:
                summary["recommendations"].append("💻 Consider technical architecture review")
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get project summary for {project_id}: {str(e)}")
            return {"error": str(e)}
    
    async def trigger_batch_analysis(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """Trigger batch analysis for multiple tensions"""
        
        try:
            # Get tensions to analyze
            if project_id:
                tensions = await self.tension_repo.get_by_project_id(project_id)
            else:
                # Get recent tensions (last 24 hours)
                tensions = await self.tension_repo.get_recent_tensions(limit=50)
            
            # Create reasoning requests
            requests = []
            for tension in tensions:
                context = await self._build_tension_context(tension)
                request = ReasoningRequest(
                    tension_id=tension.id,
                    title=tension.title,
                    description=tension.description or "",
                    current_status=tension.status,
                    context=context
                )
                requests.append(request)
            
            # Process batch
            results = await self.reasoning_coordinator.process_batch_tensions(requests)
            
            # Apply results
            for result in results:
                if result.success:
                    tension = next((t for t in tensions if t.id == result.tension_id), None)
                    if tension:
                        await self._apply_reasoning_results(tension, result)
            
            # Summary
            successful = sum(1 for r in results if r.success)
            
            return {
                "status": "completed",
                "total_processed": len(results),
                "successful": successful,
                "failed": len(results) - successful,
                "project_id": project_id
            }
            
        except Exception as e:
            self.logger.error(f"Batch analysis failed: {str(e)}")
            return {"error": str(e)} 