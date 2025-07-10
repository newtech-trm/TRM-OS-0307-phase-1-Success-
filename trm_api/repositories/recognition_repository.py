from typing import Optional, List, Dict, Any
from neomodel import db

from trm_api.models.recognition import RecognitionCreate, RecognitionUpdate
from trm_api.graph_models.recognition import Recognition as GraphRecognition
from trm_api.graph_models.win import WIN as GraphWIN

class RecognitionRepository:
    """
    AGE Recognition Repository - Pure semantic recognition operations
    
    AGE Philosophy: Recognition drives strategic intelligence without user dependencies.
    """

    @db.transaction
    def create_recognition(self, recognition_data: RecognitionCreate) -> GraphRecognition:
        """
        Creates new Recognition through AGE semantic orchestration
        
        AGE Philosophy: Recognition is a semantic action that validates strategic value.
        """
        # Convert Pydantic model to dictionary for graph model
        data = recognition_data.model_dump(by_alias=True)
        
        # Create the Recognition node through AGE orchestration
        recognition = GraphRecognition(**data).save()
        
        # NOTE: In AGE architecture, Recognition is autonomous semantic validation
        # No user relationship dependencies needed - Recognition validates itself
        
        # Establish relationship with WIN (RECOGNIZES) - Core AGE semantic relationship
        try:
            win = GraphWIN.nodes.get(uid=recognition_data.win_id)
            recognition.recognizes_win.connect(win)
        except GraphWIN.DoesNotExist:
            # WIN doesn't exist, but Recognition can exist independently for future connection
            pass
        
        return recognition

    def get_recognition_by_uid(self, uid: str) -> Optional[GraphRecognition]:
        """
        Retrieves Recognition by UID - AGE semantic retrieval
        
        AGE Philosophy: Recognition retrieval serves strategic intelligence.
        """
        try:
            return GraphRecognition.nodes.get(uid=uid)
        except GraphRecognition.DoesNotExist:
            return None

    def list_recognitions(self, skip: int = 0, limit: int = 100) -> List[GraphRecognition]:
        """
        Lists all Recognition nodes - AGE semantic intelligence
        
        AGE Philosophy: Recognition patterns reveal strategic insights.
        """
        return GraphRecognition.nodes.all()[skip:skip+limit]
    
    def list_recognitions_by_win(self, win_id: str, skip: int = 0, limit: int = 100) -> List[GraphRecognition]:
        """
        Lists Recognition nodes for specific WIN - AGE strategic correlation
        
        AGE Philosophy: Recognition-WIN relationships show strategic validation patterns.
        """
        return GraphRecognition.nodes.filter(winId=win_id)[skip:skip+limit]
    
    def list_recognitions_by_semantic_context(self, context_type: str, skip: int = 0, limit: int = 100) -> List[GraphRecognition]:
        """
        Lists Recognition nodes by semantic context - AGE intelligence pattern
        
        AGE Philosophy: Semantic context drives Recognition intelligence classification.
        """
        query = """
        MATCH (r:Recognition)
        WHERE r.semanticContext = $context_type OR $context_type IN r.contextTags
        RETURN r
        ORDER BY r.createdAt DESC
        SKIP $skip LIMIT $limit
        """
        results, meta = db.cypher_query(
            query, 
            {"context_type": context_type, "skip": skip, "limit": limit}
        )
        
        return [GraphRecognition.inflate(row[0]) for row in results]
    
    def list_recognitions_by_strategic_value(self, min_value: float, skip: int = 0, limit: int = 100) -> List[GraphRecognition]:
        """
        Lists Recognition nodes by strategic value threshold - AGE value intelligence
        
        AGE Philosophy: Strategic value drives Recognition prioritization.
        """
        query = """
        MATCH (r:Recognition)
        WHERE r.strategicValue >= $min_value
        RETURN r
        ORDER BY r.strategicValue DESC, r.createdAt DESC
        SKIP $skip LIMIT $limit
        """
        results, meta = db.cypher_query(
            query, 
            {"min_value": min_value, "skip": skip, "limit": limit}
        )
        
        return [GraphRecognition.inflate(row[0]) for row in results]

    def update_recognition(self, uid: str, update_data: RecognitionUpdate) -> Optional[GraphRecognition]:
        """
        Updates Recognition through AGE semantic enhancement
        
        AGE Philosophy: Recognition evolution enhances strategic intelligence.
        """
        recognition = self.get_recognition_by_uid(uid)
        if not recognition:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(recognition, key, value)
        
        recognition.save()
        return recognition

    def delete_recognition(self, uid: str) -> bool:
        """
        Deletes Recognition through AGE semantic cleanup
        
        AGE Philosophy: Recognition deletion serves strategic optimization.
        """
        recognition = self.get_recognition_by_uid(uid)
        if not recognition:
            return False
        
        recognition.delete()
        return True

    def get_recognition_strategic_analytics(self, win_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get strategic analytics for Recognition patterns - AGE intelligence
        
        AGE Philosophy: Recognition analytics reveal strategic insights and patterns.
        """
        base_query = """
        MATCH (r:Recognition)
        {}
        RETURN 
            count(r) as total_recognitions,
            avg(r.strategicValue) as avg_strategic_value,
            max(r.strategicValue) as max_strategic_value,
            min(r.strategicValue) as min_strategic_value,
            collect(DISTINCT r.recognitionType) as recognition_types,
            collect(DISTINCT r.semanticContext) as semantic_contexts
        """
        
        where_clause = "WHERE r.winId = $win_id" if win_id else ""
        query = base_query.format(where_clause)
        
        params = {"win_id": win_id} if win_id else {}
        results, meta = db.cypher_query(query, params)
        
        if results:
            row = results[0]
            return {
                "total_recognitions": row[0],
                "avg_strategic_value": float(row[1]) if row[1] else 0.0,
                "max_strategic_value": float(row[2]) if row[2] else 0.0,
                "min_strategic_value": float(row[3]) if row[3] else 0.0,
                "recognition_types": row[4] or [],
                "semantic_contexts": row[5] or [],
                "strategic_insights": "AGE Recognition intelligence analytics"
            }
        
        return {
            "total_recognitions": 0,
            "strategic_insights": "No Recognition data available for analysis"
        }
