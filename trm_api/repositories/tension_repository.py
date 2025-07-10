#!/usr/bin/env python3
"""
Tension Repository - AGE Semantic Architecture
"""

from typing import List, Optional, Dict, Any
from neomodel import DoesNotExist

from trm_api.graph_models.tension import Tension as GraphTension
from trm_api.models.tension import TensionCreate, TensionUpdate

# AGE Semantic Ontology Imports
from trm_api.graph_models.strategic_project import GraphStrategicProject  # Replaced legacy Project
# TODO: Implement AGEActor ontology integration
# from trm_api.ontology.age_actor import AGEActor  # Future implementation

from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class TensionRepository:
    """AGE Tension Repository - Strategic tension resolution"""
    
    def create_tension(self, tension_data: TensionCreate) -> Optional[GraphTension]:
        """Create strategic tension in AGE context"""
        try:
            tension = GraphTension(
                title=tension_data.title,
                description=tension_data.description,
                tension_type=tension_data.tension_type,
                severity=tension_data.severity or "medium",
                status=tension_data.status or "identified",
                impact_scope=tension_data.impact_scope or "localized",
                strategic_priority=tension_data.strategic_priority or "medium",
                identified_date=tension_data.identified_date,
                resolution_target_date=tension_data.resolution_target_date,
                stakeholders_affected=tension_data.stakeholders_affected or [],
                root_causes=tension_data.root_causes or [],
                potential_solutions=tension_data.potential_solutions or [],
                strategic_context=tension_data.strategic_context or {}
            ).save()
            
            logger.info(f"AGE Strategic Tension created: {tension.uid} - {tension.title}")
            return tension
            
        except Exception as e:
            logger.error(f"AGE Tension creation error: {str(e)}")
            return None

    def get_tension_by_id(self, tension_id: str) -> Optional[GraphTension]:
        """Get strategic tension by ID"""
        try:
            return GraphTension.nodes.get_or_none(uid=tension_id)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"AGE Tension retrieval error: {str(e)}")
            return None

    def list_tensions(self, skip: int = 0, limit: int = 100) -> List[GraphTension]:
        """List strategic tensions"""
        try:
            tensions = GraphTension.nodes.all()[skip:skip+limit]
            logger.info(f"AGE Tension Repository: Listed {len(tensions)} strategic tensions")
            return tensions
        except Exception as e:
            logger.error(f"AGE Tension listing error: {str(e)}")
            return []

    def update_tension(self, uid: str, tension_data: TensionUpdate) -> Optional[GraphTension]:
        """Update strategic tension"""
        try:
            tension = self.get_tension_by_id(uid)
            if not tension:
                return None
            
            update_fields = tension_data.dict(exclude_unset=True)
            for field, value in update_fields.items():
                if hasattr(tension, field):
                    setattr(tension, field, value)
            
            tension.save()
            logger.info(f"AGE Strategic Tension updated: {tension.uid}")
            return tension
            
        except Exception as e:
            logger.error(f"AGE Tension update error: {str(e)}")
            return None

    def delete_tension(self, uid: str) -> bool:
        """Delete strategic tension"""
        try:
            tension = self.get_tension_by_id(uid)
            if tension:
                tension.delete()
                logger.info(f"AGE Strategic Tension deleted: {uid}")
                return True
            return False
        except Exception as e:
            logger.error(f"AGE Tension deletion error: {str(e)}")
            return False
