import uuid
from neo4j import Driver
from typing import List, Optional, Dict, Any
from datetime import datetime

from trm_api.db.session import get_driver
from trm_api.models.resource import (
    Resource, ResourceBase, ResourceInDB,
    ResourceType, FinancialResourceCreate, KnowledgeResourceCreate,
    HumanResourceCreate, ToolResourceCreate, EquipmentResourceCreate,
    SpaceResourceCreate
)
from trm_api.services.utils import process_record, process_records, process_relationship_record
from trm_api.models.relationships import Relationship


class ResourceService:
    """
    Service layer for handling business logic related to Resources.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def create_resource(self, resource_create: ResourceBase) -> Optional[Resource]:
        """Creates a new Resource node with type-specific details."""
        params = resource_create.model_dump(by_alias=True)

        # Ensure 'details' is a dict. model_dump should handle this correctly for both
        # Pydantic model details (dumps to dict) and dict details (includes as is).
        # If 'details' could be None after dump (e.g. from an Optional field not provided),
        # ensure it's an empty dict.
        if not isinstance(params.get("details"), dict):
            params["details"] = {}

        # Generate a unique resource ID, this will be mapped to 'uid' by process_record
        params["resourceId"] = str(uuid.uuid4())
        
        # Set creation and update timestamps
        now = datetime.utcnow()
        params["createdAt"] = now
        params["updatedAt"] = now

        with self._get_db().session() as session:
            result_properties = session.execute_write(self._create_resource_tx, params)
            
            if result_properties:
                # result_properties is from process_record, should align with ResourceInDB fields
                # (uid, createdAt, updatedAt as Python datetime, details as dict)
                return Resource(**result_properties)
            return None

    @staticmethod
    def _create_resource_tx(tx, params: dict) -> Optional[dict]:
        # Base properties for the Resource node
        resource_props_list = [
            "resourceId: $resourceId",
            "name: $name",
            "description: $description",
            "resourceType: $resourceType",
            "status: $status",
            "createdAt: datetime($createdAt)", # Neo4j temporal type
            "updatedAt: datetime($updatedAt)", # Neo4j temporal type
            "details: $details" # $details is expected to be a map/dictionary
        ]

        # Conditionally add ownerAgentId if present and not None in params
        if params.get("ownerAgentId") is not None:
            resource_props_list.append("ownerAgentId: $ownerAgentId")

        # Construct the SET part of the query
        resource_props_str = ", ".join(resource_props_list)
        
        query = (
            f"CREATE (r:Resource {{ {resource_props_str} }}) "
            "RETURN r"
        )
        
        result = tx.run(query, params)
        record = result.single()
        # process_record should handle Neo4j datetime to Python datetime conversion
        # and map 'resourceId' to 'uid' for Pydantic model compatibility.
        return process_record(record) if record else None
    
    def create_financial_resource(self, resource_create: FinancialResourceCreate) -> Resource:
        """Creates a new Financial resource."""
        return self.create_resource(resource_create)
    
    def create_knowledge_resource(self, resource_create: KnowledgeResourceCreate) -> Resource:
        """Creates a new Knowledge resource."""
        return self.create_resource(resource_create)
    
    def create_human_resource(self, resource_create: HumanResourceCreate) -> Resource:
        """Creates a new Human resource."""
        return self.create_resource(resource_create)
    
    def create_tool_resource(self, resource_create: ToolResourceCreate) -> Resource:
        """Creates a new Tool resource."""
        return self.create_resource(resource_create)
    
    def create_equipment_resource(self, resource_create: EquipmentResourceCreate) -> Resource:
        """Creates a new Equipment resource."""
        return self.create_resource(resource_create)
    
    def create_space_resource(self, resource_create: SpaceResourceCreate) -> Resource:
        """Creates a new Space resource."""
        return self.create_resource(resource_create)

    def get_resource_by_id(self, resource_id: str) -> Optional[Resource]:
        """Retrieves a single resource by its unique ID."""
        with self._get_db().session() as session:
            result = session.execute_read(self._get_resource_by_id_tx, resource_id)
            return Resource(**result) if result else None

    @staticmethod
    def _get_resource_by_id_tx(tx, resource_id: str) -> Optional[dict]:
        query = "MATCH (r:Resource {resourceId: $resourceId}) RETURN r"
        result = tx.run(query, resourceId=resource_id)
        record = result.single()
        return process_record(record) if record else None

    def list_resources(self, skip: int = 0, limit: int = 100, resource_type: Optional[ResourceType] = None) -> List[Resource]:
        """Retrieves a list of resources with optional type filtering and pagination."""
        with self._get_db().session() as session:
            results = session.execute_read(self._list_resources_tx, skip, limit, resource_type.value if resource_type else None)
            return [Resource(**result) for result in results if result]

    @staticmethod
    def _list_resources_tx(tx, skip: int, limit: int, resource_type: Optional[str] = None) -> List[dict]:
        params = {"skip": skip, "limit": limit}
        
        if resource_type:
            query = (
                "MATCH (r:Resource) "
                "WHERE r.resourceType = $resourceType "
                "RETURN r "
                "ORDER BY r.name ASC "
                "SKIP $skip LIMIT $limit"
            )
            params["resourceType"] = resource_type
        else:
            query = (
                "MATCH (r:Resource) "
                "RETURN r "
                "ORDER BY r.name ASC "
                "SKIP $skip LIMIT $limit"
            )
        
        result = tx.run(query, params)
        return [process_record(record) for record in result]

    def update_resource(self, resource_id: str, update_data: Dict[str, Any]) -> Optional[Resource]:
        """Updates an existing resource."""
        if not update_data:
            return self.get_resource_by_id(resource_id)

        # Add updated timestamp
        update_data['updatedAt'] = datetime.utcnow()

        with self._get_db().session() as session:
            result = session.execute_write(self._update_resource_tx, resource_id, update_data)
            return Resource(**result) if result else None

    @staticmethod
    def _update_resource_tx(tx, resource_id: str, update_data: dict) -> Optional[dict]:
        # Prepare SET clauses for standard properties
        standard_fields = [key for key in update_data.keys() if key != 'details']
        set_clauses = [f"r.{key} = ${key}" for key in standard_fields]
        
        # Handle updated timestamp as datetime
        if 'updatedAt' in update_data:
            set_clauses.remove('r.updatedAt = $updatedAt')
            set_clauses.append('r.updatedAt = datetime($updatedAt)')
        
        # Handle details as a separate update if it exists
        if 'details' in update_data:
            set_clauses.append('r.details = $details')
        
        query = (
            f"MATCH (r:Resource {{resourceId: $resourceId}}) "
            f"SET {', '.join(set_clauses)} "
            "RETURN r"
        )
        
        params = {'resourceId': resource_id, **update_data}
        result = tx.run(query, params)
        record = result.single()
        return process_record(record) if record else None

    def delete_resource(self, resource_id: str) -> bool:
        """Deletes a resource by its ID."""
        with self._get_db().session() as session:
            result = session.execute_write(self._delete_resource_tx, resource_id)
            return result

    @staticmethod
    def _delete_resource_tx(tx, resource_id: str) -> bool:
        query = "MATCH (r:Resource {resourceId: $resourceId}) DETACH DELETE r"
        result = tx.run(query, resourceId=resource_id)
        summary = result.consume()
        return summary.counters.nodes_deleted > 0
    
    def assign_resource_to_project(self, resource_id: str, project_id: str) -> Optional[Relationship]:
        """Assigns a resource to a project, creating a HAS_RESOURCE relationship."""
        with self._get_db().session() as session:
            result = session.execute_write(self._assign_resource_to_project_tx, resource_id, project_id)
            return Relationship(**result) if result else None

    @staticmethod
    def _assign_resource_to_project_tx(tx, resource_id: str, project_id: str) -> Optional[dict]:
        query = (
            "MATCH (r:Resource {resourceId: $resourceId}) "
            "MATCH (p:Project {projectId: $projectId}) "
            "MERGE (p)-[rel:HAS_RESOURCE]->(r) "
            "ON CREATE SET rel.createdAt = datetime() "
            "RETURN "
            "    p.projectId AS source_id, "
            "    labels(p)[0] AS source_type, "
            "    r.resourceId AS target_id, "
            "    labels(r)[0] AS target_type, "
            "    type(rel) AS type, "
            "    rel.createdAt as createdAt"
        )
        result = tx.run(query, resourceId=resource_id, projectId=project_id)
        record = result.single()
        return process_relationship_record(record) if record else None
    
    def assign_resource_to_task(self, resource_id: str, task_id: str) -> Optional[Relationship]:
        """Assigns a resource to a task, creating a USES_RESOURCE relationship."""
        with self._get_db().session() as session:
            result = session.execute_write(self._assign_resource_to_task_tx, resource_id, task_id)
            return Relationship(**result) if result else None

    @staticmethod
    def _assign_resource_to_task_tx(tx, resource_id: str, task_id: str) -> Optional[dict]:
        query = (
            "MATCH (r:Resource {resourceId: $resourceId}) "
            "MATCH (t:Task {taskId: $taskId}) "
            "MERGE (t)-[rel:USES_RESOURCE]->(r) "
            "ON CREATE SET rel.createdAt = datetime() "
            "RETURN "
            "    t.taskId AS source_id, "
            "    labels(t)[0] AS source_type, "
            "    r.resourceId AS target_id, "
            "    labels(r)[0] AS target_type, "
            "    type(rel) AS type, "
            "    rel.createdAt as createdAt"
        )
        result = tx.run(query, resourceId=resource_id, taskId=task_id)
        record = result.single()
        return process_relationship_record(record) if record else None


# Singleton instance of the service
resource_service = ResourceService()
