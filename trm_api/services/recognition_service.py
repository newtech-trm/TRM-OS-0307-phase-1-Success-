#!/usr/bin/env python3
"""
Recognition Service - AGE Semantic Architecture
Handles Recognition phase của Recognition → Event → WIN pattern

ELIMINATED: Legacy Agent, Project, Resource CRUD models
REPLACED: AGEActor, StrategicUnit, CoordinatedResource semantic ontology
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from neomodel import DoesNotExist

from trm_api.graph_models.recognition import Recognition as GraphRecognition
from trm_api.models.recognition import RecognitionCreate, RecognitionUpdate, Recognition

# AGE Semantic Ontology Imports
from trm_api.ontology.age_actor import AGEActor  # Replaced AgentGraphModel
from trm_api.ontology.strategic_unit import StrategicUnit  # Replaced ProjectGraphModel
# TODO: Implement CoordinatedResource ontology model
# from trm_api.ontology.coordinated_resource import CoordinatedResource  # Future implementation

from trm_api.graph_models.win import WIN as GraphWIN
from trm_api.repositories.recognition_repository import RecognitionRepository
from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)

class RecognitionService:
    """
    AGE Recognition Service - Semantic recognition processing
    Handles the Recognition phase of Recognition → Event → WIN cycle
    """
    
    def __init__(self):
        self.repository = RecognitionRepository()
    
    def create_recognition(self, recognition_data: RecognitionCreate) -> Optional[Recognition]:
        """Create strategic recognition using AGE semantic ontology"""
        try:
            logger.info(f"AGE Recognition Service: Creating strategic recognition for type: {recognition_data.recognition_type}")
            
            # Create recognition using AGE semantic context
            graph_recognition = self.repository.create_recognition(recognition_data)
            
            if graph_recognition:
                # Convert to semantic Recognition model
                recognition = Recognition(
                    uid=graph_recognition.uid,
                    recognition_type=graph_recognition.recognition_type,
                    title=graph_recognition.title,
                    description=graph_recognition.description,
                    status=graph_recognition.status,
                    recognition_value=graph_recognition.recognition_value,
                    strategic_impact=graph_recognition.strategic_impact,
                    created_at=graph_recognition.created_at,
                    updated_at=graph_recognition.updated_at
                )
                
                logger.info(f"AGE Recognition created successfully: {recognition.uid}")
                return recognition
            else:
                logger.error("Failed to create recognition in AGE system")
                return None
                
        except Exception as e:
            logger.error(f"AGE Recognition Service error: {str(e)}")
            return None

    def get_recognition_by_id(self, recognition_id: str) -> Optional[Recognition]:
        """Get recognition by ID with AGE semantic context"""
        try:
            graph_recognition = self.repository.get_recognition_by_id(recognition_id)
            
            if graph_recognition:
                return Recognition(
                    uid=graph_recognition.uid,
                    recognition_type=graph_recognition.recognition_type,
                    title=graph_recognition.title,
                    description=graph_recognition.description,
                    status=graph_recognition.status,
                    recognition_value=graph_recognition.recognition_value,
                    strategic_impact=graph_recognition.strategic_impact,
                    created_at=graph_recognition.created_at,
                    updated_at=graph_recognition.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"AGE Recognition retrieval error: {str(e)}")
            return None

    def update_recognition(self, recognition_id: str, update_data: RecognitionUpdate) -> Optional[Recognition]:
        """Update recognition with AGE semantic enhancements"""
        try:
            updated_graph = self.repository.update_recognition(recognition_id, update_data)
            
            if updated_graph:
                return Recognition(
                    uid=updated_graph.uid,
                    recognition_type=updated_graph.recognition_type,
                    title=updated_graph.title,
                    description=updated_graph.description,
                    status=updated_graph.status,
                    recognition_value=updated_graph.recognition_value,
                    strategic_impact=updated_graph.strategic_impact,
                    created_at=updated_graph.created_at,
                    updated_at=updated_graph.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"AGE Recognition update error: {str(e)}")
            return None

    def delete_recognition(self, recognition_id: str) -> bool:
        """Delete recognition with AGE semantic validation"""
        try:
            return self.repository.delete_recognition(recognition_id)
        except Exception as e:
            logger.error(f"AGE Recognition deletion error: {str(e)}")
            return False

    def list_recognitions(self, skip: int = 0, limit: int = 100) -> List[Recognition]:
        """List recognitions with AGE semantic context"""
        try:
            graph_recognitions = self.repository.list_recognitions(skip=skip, limit=limit)
            
            recognitions = []
            for graph_recognition in graph_recognitions:
                recognition = Recognition(
                    uid=graph_recognition.uid,
                    recognition_type=graph_recognition.recognition_type,
                    title=graph_recognition.title,
                    description=graph_recognition.description,
                    status=graph_recognition.status,
                    recognition_value=graph_recognition.recognition_value,
                    strategic_impact=graph_recognition.strategic_impact,
                    created_at=graph_recognition.created_at,
                    updated_at=graph_recognition.updated_at
                )
                recognitions.append(recognition)
                
            logger.info(f"AGE Recognition Service: Listed {len(recognitions)} strategic recognitions")
            return recognitions
            
        except Exception as e:
            logger.error(f"AGE Recognition listing error: {str(e)}")
            return []

    def get_strategic_recognitions_analytics(self) -> Dict[str, Any]:
        """Get strategic recognition analytics using AGE intelligence"""
        try:
            all_recognitions = self.list_recognitions(limit=1000)
            
            analytics = {
                "total_recognitions": len(all_recognitions),
                "recognition_types": {},
                "status_distribution": {},
                "average_strategic_impact": 0.0,
                "total_recognition_value": 0.0,
                "age_insights": {
                    "high_impact_recognitions": 0,
                    "strategic_patterns": [],
                    "recommendation": ""
                }
            }
            
            total_impact = 0.0
            total_value = 0.0
            high_impact_count = 0
            
            for recognition in all_recognitions:
                # Recognition types
                rec_type = recognition.recognition_type
                analytics["recognition_types"][rec_type] = analytics["recognition_types"].get(rec_type, 0) + 1
                
                # Status distribution
                status = recognition.status
                analytics["status_distribution"][status] = analytics["status_distribution"].get(status, 0) + 1
                
                # Impact and value aggregation
                if recognition.strategic_impact:
                    total_impact += recognition.strategic_impact
                    if recognition.strategic_impact >= 0.8:
                        high_impact_count += 1
                
                if recognition.recognition_value:
                    total_value += recognition.recognition_value
            
            # Calculate averages
            if len(all_recognitions) > 0:
                analytics["average_strategic_impact"] = total_impact / len(all_recognitions)
                analytics["total_recognition_value"] = total_value
                
                # AGE insights
                analytics["age_insights"]["high_impact_recognitions"] = high_impact_count
                
                # Strategic patterns detection
                if high_impact_count > 0:
                    analytics["age_insights"]["strategic_patterns"].append("High-impact recognition pattern detected")
                
                # AGE recommendation
                if analytics["average_strategic_impact"] < 0.5:
                    analytics["age_insights"]["recommendation"] = "Consider reviewing recognition criteria to increase strategic impact"
                else:
                    analytics["age_insights"]["recommendation"] = "Strong strategic recognition performance"
            
            logger.info(f"AGE Recognition Analytics: {analytics['total_recognitions']} recognitions analyzed")
            return analytics
            
        except Exception as e:
            logger.error(f"AGE Recognition analytics error: {str(e)}")
            return {
                "error": "Failed to generate AGE recognition analytics",
                "total_recognitions": 0
            }

# Create service instance for import
recognition_service = RecognitionService()
