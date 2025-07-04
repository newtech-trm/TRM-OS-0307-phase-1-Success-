from neo4j import Driver
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import uuid
import traceback
import asyncio
import logging

logger = logging.getLogger(__name__)

from trm_api.db.session import get_driver
from trm_api.models.relationships import Relationship, RelationshipType, TargetEntityTypeEnum
from trm_api.services.utils import process_relationship_record
from trm_api.services.constants import EntityTypeKindMapping
from trm_api.adapters.datetime_adapter import normalize_dict_datetimes


class RelationshipService:
    """
    Service layer for handling business logic related to Relationships.
    This service handles creation, querying, and management of all relationship types.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def create_relationship(
        self,
        source_id: str,
        source_type: TargetEntityTypeEnum,
        target_id: str,
        target_type: TargetEntityTypeEnum,
        relationship_type: RelationshipType,
        relationship_property: Optional[Dict[str, Any]] = None,
        relationship_properties: Optional[Dict[str, Any]] = None,
    ) -> Optional[Union[Relationship, Dict[str, Any]]]:
        """
        Creates a relationship between two entities.
        
        Args:
            source_id: The ID of the source entity
            source_type: The type of the source entity
            target_id: The ID of the target entity
            target_type: The type of the target entity
            relationship_type: The type of relationship to create
            relationship_property: Optional properties to set on the relationship
            relationship_properties: Alias for relationship_property (cho tương thích ngược)
            
        Returns:
            The created relationship or None if creation failed
        """
        # Gộp properties từ cả hai tham số (nếu có) để đảm bảo tương thích ngược
        properties = {}
        if relationship_property is not None:
            properties.update(relationship_property)
        if relationship_properties is not None:
            properties.update(relationship_properties)
            
        db = self._get_db()
        with db.session() as session:
            result = session.execute_write(
                self._create_relationship_tx,
                source_id,
                source_type,
                target_id,
                target_type,
                relationship_type,
                properties or None
            )
            return result

    @staticmethod
    def _create_relationship_tx(
        tx,
        source_id: str,
        source_type: TargetEntityTypeEnum,
        target_id: str,
        target_type: TargetEntityTypeEnum,
        relationship_type: RelationshipType,
        relationship_property: Optional[Dict[str, Any]] = None,
    ) -> Optional[Union[Relationship, Dict[str, Any]]]:
        """
        Transaction function for creating a relationship.
        Uses dynamic labels based on the entity types.
        """
        query = (
            "MATCH (source) "
            "WHERE (source:{source_type}) AND "
            "(source.{source_id_field} = $source_id OR source.uid = $source_id) "
            "MATCH (target) "
            "WHERE (target:{target_type}) AND "
            "(target.{target_id_field} = $target_id OR target.uid = $target_id) "
            "MERGE (source)-[rel:{rel_type}]->(target) "
            "ON CREATE SET rel.createdAt = datetime() "
            "SET rel.createdAt = COALESCE(rel.createdAt, datetime()) "
            "RETURN "
            "    source.uid AS source_id, "
            "    '{source_type}' AS source_type, "
            "    target.uid AS target_id, "
            "    '{target_type}' AS target_type, "
            "    type(rel) AS type, "
            "    rel.createdAt as createdAt"
        )

        # Map entity types to their ID field names (based on convention)
        id_field_map = {
            "User": "userId",
            "Team": "teamId",
            "Project": "projectId",
            "Task": "taskId",
            "Tension": "tensionId",
            "Win": "winId",
            "KnowledgeSnippet": "snippetId",
            "Skill": "skillId",
            "Recognition": "recognitionId",
            "Resource": "resourceId",
            "Agent": "agentId",
            "Event": "eventId",
            "Tool": "toolId"
        }

        # Format query with the right labels and ID fields  
        # Map enum values to actual Neo4j labels
        label_mapping = {
            "Win": "WIN",  # TargetEntityTypeEnum.WIN.value = "Win" but Neo4j label is "WIN"
            "KnowledgeSnippet": "KnowledgeSnippet",  # This should match
            "Agent": "Agent",
            "Project": "Project", 
            "Task": "Task",
            "Event": "Event",
            "Recognition": "Recognition",
            "Tension": "Tension",
            "Resource": "Resource"
        }
        
        source_type_value = source_type.value if isinstance(source_type, TargetEntityTypeEnum) else source_type
        target_type_value = target_type.value if isinstance(target_type, TargetEntityTypeEnum) else target_type
        rel_type_value = relationship_type.value if isinstance(relationship_type, RelationshipType) else relationship_type
        
        # Apply label mapping
        source_label = label_mapping.get(source_type_value, source_type_value)
        target_label = label_mapping.get(target_type_value, target_type_value)

        source_id_field = id_field_map.get(source_type_value, "uid")
        target_id_field = id_field_map.get(target_type_value, "uid")

        formatted_query = query.format(
            source_type=source_label,
            source_id_field=source_id_field,
            target_type=target_label,
            target_id_field=target_id_field,
            rel_type=rel_type_value
        )

        logger.debug("===== RELATIONSHIP CREATION DEBUG =====")
        logger.debug("Source: %s -> %s (ID: %s)", source_type_value, source_label, source_id)
        logger.debug("Target: %s -> %s (ID: %s)", target_type_value, target_label, target_id)
        logger.debug("Relationship: %s", rel_type_value)
        logger.debug("Query: %s", formatted_query)
        logger.debug("=======================================")

        result = tx.run(
            formatted_query,
            source_id=source_id,
            target_id=target_id,
        )
        record = result.single()
        
        if record:
            # Chuyển đổi neo4j.time.DateTime sang python datetime
            created_at = record["createdAt"]
            if created_at and hasattr(created_at, 'to_native'):
                created_at = created_at.to_native()
            
            # Tạo dictionary từ record và thêm các thuộc tính bổ sung từ relationship_property
            result_dict = {
                "source_id": record["source_id"],
                "source_type": record["source_type"],
                "target_id": record["target_id"],
                "target_type": record["target_type"],
                "type": record["type"],
                "createdAt": created_at
            }
            
            # Thêm các thuộc tính từ relationship_property nếu có
            if relationship_property:
                for key, value in relationship_property.items():
                    if key not in result_dict:
                        result_dict[key] = value
            
            try:
                # Tạo đối tượng Relationship từ dictionary
                relationship_obj = Relationship(**result_dict)
                return relationship_obj
            except Exception as e:
                logging.warning(f"Không thể tạo đối tượng Relationship, trả về dictionary: {str(e)}")
                # Nếu không tạo được đối tượng Relationship, trả về dictionary
                return normalize_dict_datetimes(result_dict)
        return None

    def get_relationships(
        self,
        entity_id: str,
        entity_type: str,
        direction: str = "outgoing",
        relationship_type: Optional[RelationshipType] = None,
        related_entity_type: Optional[TargetEntityTypeEnum] = None,
    ) -> List[Union[Relationship, Dict[str, Any]]]:
        """Lấy các mối quan hệ của một thực thể. Được thiết kế để xử lý linh hoạt mọi đầu vào."""
        """
        Gets all relationships for a specific entity.
        
        Args:
            entity_id: The ID of the entity, if None returns all relationships
            entity_type: The type of the entity, if None returns all relationships
            direction: "outgoing" for relationships where the entity is the source,
                       "incoming" for relationships where the entity is the target,
                       "both" for relationships in both directions
            relationship_type: Optional filter for a specific relationship type
            related_entity_type: Optional filter for a specific related entity type
            
        Returns:
            A list of relationships for the entity
        """
        # Ghi log chi tiết các tham số
        logger.debug("===== GET RELATIONSHIPS PARAMS =====")
        logger.debug("entity_id: %s", entity_id)
        logger.debug("entity_type: %s", entity_type)
        logger.debug("direction: %s", direction)
        logger.debug("relationship_type: %s", relationship_type)
        logger.debug("related_entity_type: %s", related_entity_type)
        logger.debug("==================================")
        
        # Nếu không có entity_id hoặc entity_type, trả về danh sách rỗng ngay lập tức
        if not entity_id or not entity_type:
            logger.debug("Trả về danh sách rỗng vì entity_id hoặc entity_type bị thiếu")
            return []

        # Chuyển đổi entity_type thành string nếu cần
        try:
            if isinstance(entity_type, str):
                entity_type_mapped = EntityTypeKindMapping.get(entity_type, entity_type)
            else:
                # Nếu là enum hoặc kiểu khác, thử chuyển thành string
                entity_type_str = str(entity_type)
                entity_type_mapped = EntityTypeKindMapping.get(entity_type_str, entity_type_str)
                
            logger.debug("Đã chuyển đổi entity_type: %s -> %s", entity_type, entity_type_mapped)
        except Exception as e:
            logger.error("Lỗi khi chuyển đổi entity_type: %s", str(e))
            return []

        try:
            db = self._get_db()
            with db.session() as session:
                result = session.execute_read(
                    self._get_relationships_tx,
                    entity_id,
                    entity_type_mapped,
                    direction,
                    relationship_type,
                    related_entity_type
                )
                return result
        except Exception as e:
            logger.error("===== LỖI KHI LẤY RELATIONSHIPS =====")
            logger.error(str(e))
            logger.error("Traceback: %s", traceback.format_exc())
            logger.error("=============================")
            return []

    @staticmethod
    def _get_relationships_tx(
        tx,
        entity_id: str,
        entity_type: str,
        direction: str,
        relationship_type: Optional[RelationshipType],
        related_entity_type: Optional[TargetEntityTypeEnum]
    ) -> List[Union[Relationship, Dict[str, Any]]]:
        """
        Transaction function for getting relationships.
        """
        # Map entity types to their ID field names
        id_field_map = {
            "User": "userId",
            "Team": "teamId",
            "Project": "projectId",
            "Task": "taskId",
            "Tension": "tensionId",
            "Win": "winId",
            "KnowledgeSnippet": "snippetId",
            "Skill": "skillId",
            "Recognition": "recognitionId",
            "Resource": "resourceId",
            "Agent": "agentId",
            "Event": "eventId",
            "Tool": "toolId"
        }

        entity_type_value = entity_type.value if isinstance(entity_type, TargetEntityTypeEnum) else entity_type
        entity_id_field = id_field_map.get(entity_type_value, "uid")
        rel_type = relationship_type.value if isinstance(relationship_type, RelationshipType) else relationship_type
        related_type = related_entity_type.value if isinstance(related_entity_type, TargetEntityTypeEnum) else related_entity_type

        # Build the query based on direction and filters
        if direction == "outgoing":
            query_template = (
                "MATCH (entity:{entity_type})-[rel{rel_filter}]->(related{related_filter}) "
                "WHERE entity.{id_field} = $entity_id OR entity.uid = $entity_id "
                "RETURN "
                "    entity.uid AS source_id, "
                "    '{entity_type}' AS source_type, "
                "    related.uid AS target_id, "
                "    labels(related)[0] AS target_type, "
                "    type(rel) AS type, "
                "    CASE WHEN rel.createdAt IS NOT NULL THEN rel.createdAt ELSE datetime() END AS createdAt"
            )
        elif direction == "incoming":
            query_template = (
                "MATCH (related{related_filter})-[rel{rel_filter}]->(entity:{entity_type}) "
                "WHERE entity.{id_field} = $entity_id OR entity.uid = $entity_id "
                "RETURN "
                "    related.uid AS source_id, "
                "    labels(related)[0] AS source_type, "
                "    entity.uid AS target_id, "
                "    '{entity_type}' AS target_type, "
                "    type(rel) AS type, "
                "    CASE WHEN rel.createdAt IS NOT NULL THEN rel.createdAt ELSE datetime() END AS createdAt"
            )
        else:  # both
            query_template = (
                "MATCH (entity:{entity_type})-[rel{rel_filter}]-(related{related_filter}) "
                "WHERE entity.{id_field} = $entity_id OR entity.uid = $entity_id "
                "RETURN "
                "    CASE WHEN startNode(rel) = entity THEN entity.uid ELSE related.uid END AS source_id, "
                "    CASE WHEN startNode(rel) = entity THEN '{entity_type}' ELSE labels(related)[0] END AS source_type, "
                "    CASE WHEN endNode(rel) = entity THEN entity.uid ELSE related.uid END AS target_id, "
                "    CASE WHEN endNode(rel) = entity THEN '{entity_type}' ELSE labels(related)[0] END AS target_type, "
                "    type(rel) AS type, "
                "    CASE WHEN rel.createdAt IS NOT NULL THEN rel.createdAt ELSE datetime() END AS createdAt"
            )

        # Add filters if specified
        rel_filter = f":{rel_type}" if rel_type else ""
        related_filter = f":{related_type}" if related_type else ""

        query = query_template.format(
            entity_type=entity_type_value,
            id_field=entity_id_field,
            rel_filter=rel_filter,
            related_filter=related_filter
        )

        result = tx.run(query, entity_id=entity_id)
        relationships = []

        for record in result:
            # Chuyển đổi neo4j.time.DateTime sang python datetime nếu cần
            created_at = record["createdAt"]
            if created_at and hasattr(created_at, 'to_native'):
                created_at = created_at.to_native()
            
            # Tạo dictionary từ record
            result_dict = {
                "source_id": record["source_id"],
                "source_type": record["source_type"],
                "target_id": record["target_id"],
                "target_type": record["target_type"],
                "type": record["type"],
                "createdAt": created_at
            }
            
            # Thêm các thuộc tính khác nếu có
            for key, value in record.items():
                if key not in result_dict and key not in ["source_id", "source_type", "target_id", "target_type", "type", "createdAt"]:
                    result_dict[key] = value
            
            try:
                # Tạo đối tượng Relationship từ dictionary
                relationship_obj = Relationship(**result_dict)
                relationships.append(relationship_obj)
            except Exception as e:
                logging.warning(f"Không thể tạo đối tượng Relationship, thêm dictionary vào kết quả: {str(e)}")
                # Nếu không tạo được đối tượng Relationship, thêm dictionary vào kết quả
                relationships.append(normalize_dict_datetimes(result_dict))
        
        return relationships

    def delete_relationship(
        self,
        source_id: str,
        source_type: TargetEntityTypeEnum,
        target_id: str,
        target_type: TargetEntityTypeEnum,
        relationship_type: RelationshipType
    ) -> bool:
        """
        Deletes a relationship between two entities.
        
        Args:
            source_id: The ID of the source entity
            source_type: The type of the source entity
            target_id: The ID of the target entity
            target_type: The type of the target entity
            relationship_type: The type of relationship to delete
            
        Returns:
            True if the relationship was deleted, False otherwise
        """
        try:
            db = self._get_db()
            with db.session() as session:
                result = session.execute_write(
                    self._delete_relationship_tx,
                    source_id,
                    source_type,
                    target_id,
                    target_type,
                    relationship_type
                )
                return result
        except Exception as e:
            logger.error("Lỗi khi xóa relationship: %s", str(e))
            logger.error("Exception traceback: %s", traceback.format_exc())
            return False

    @staticmethod
    def _delete_relationship_tx(
        tx,
        source_id: str,
        source_type: TargetEntityTypeEnum,
        target_id: str,
        target_type: TargetEntityTypeEnum,
        relationship_type: RelationshipType
    ) -> bool:
        """
        Transaction function for deleting a relationship.
        """
        # Map entity types to their ID field names
        id_field_map = {
            "User": "userId",
            "Team": "teamId",
            "Project": "projectId",
            "Task": "taskId",
            "Tension": "tensionId",
            "Win": "winId",
            "KnowledgeSnippet": "snippetId",
            "Skill": "skillId",
            "Recognition": "recognitionId",
            "Resource": "resourceId",
            "Agent": "agentId",
            "Event": "eventId",
            "Tool": "toolId"
        }

        source_type_value = source_type.value if isinstance(source_type, TargetEntityTypeEnum) else source_type
        target_type_value = target_type.value if isinstance(target_type, TargetEntityTypeEnum) else target_type
        rel_type_value = relationship_type.value if isinstance(relationship_type, RelationshipType) else relationship_type

        source_id_field = id_field_map.get(source_type_value, "uid")
        target_id_field = id_field_map.get(target_type_value, "uid")

        query = (
            f"MATCH (source:{source_type_value})-[rel:{rel_type_value}]->(target:{target_type_value}) "
            f"WHERE (source.{source_id_field} = $source_id OR source.uid = $source_id) "
            f"AND (target.{target_id_field} = $target_id OR target.uid = $target_id) "
            f"DELETE rel"
        )

        result = tx.run(
            query,
            source_id=source_id,
            target_id=target_id
        )
        summary = result.consume()
        return summary.counters.relationships_deleted > 0


# Singleton instance of the service
relationship_service = RelationshipService()
