from neo4j import Driver
from typing import List, Optional
from datetime import datetime

from trm_api.db.session import get_driver
from trm_api.models.knowledge_snippet import KnowledgeSnippet, KnowledgeSnippetCreate, KnowledgeSnippetUpdate, KnowledgeSnippetInDB

class KnowledgeSnippetService:
    """
    Service layer for handling business logic related to Knowledge Snippets.
    Includes versioning logic for updates.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def create_snippet(self, snippet_create: KnowledgeSnippetCreate) -> dict:
        """Creates a new KnowledgeSnippet node."""
        snippet_db = KnowledgeSnippetInDB(**snippet_create.model_dump())
        params = snippet_db.model_dump(by_alias=True)

        with self._get_db().session() as session:
            result = session.write_transaction(self._create_snippet_tx, params)
            # Trả về dict thay vì đối tượng Pydantic để tương thích với tests
            return result

    @staticmethod
    def _create_snippet_tx(tx, params: dict) -> dict:
        query = (
            "CREATE (ks:KnowledgeSnippet { "
            "  uid: $uid, "
            "  snippetId: $uid, " # Duy trì backwards compatibility, sử dụng uid làm snippetId
            "  content: $content, "
            "  snippetType: $snippetType, "
            "  sourceEntityId: $sourceEntityId, "
            "  tags: $tags, "
            "  version: 1, " # Initial version is 1
            "  createdAt: datetime($createdAt), "
            "  updatedAt: null "
            "}) "
            "RETURN ks"
        )
        result = tx.run(query, params)
        record = result.single()
        return dict(record['ks']) if record and record['ks'] else None

    def get_snippet_by_id(self, snippet_id: str) -> Optional[dict]:
        """Retrieves a single snippet by its unique ID."""
        with self._get_db().session() as session:
            result = session.read_transaction(self._get_snippet_by_id_tx, snippet_id)
            # Trả về dict thay vì đối tượng Pydantic để tương thích với tests
            return result

    @staticmethod
    def _get_snippet_by_id_tx(tx, snippet_id: str) -> Optional[dict]:
        # Tương thích ngược - tim kiếm cả theo uid hoặc snippetId
        query = (
            "MATCH (ks:KnowledgeSnippet) "
            "WHERE ks.uid = $id OR ks.snippetId = $id "
            "RETURN ks"
        )
        result = tx.run(query, id=snippet_id)
        record = result.single()
        return dict(record['ks']) if record and record['ks'] else None

    def list_snippets(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Retrieves a list of snippets with pagination."""
        with self._get_db().session() as session:
            results = session.read_transaction(self._list_snippets_tx, skip, limit)
            # Trả về list dict thay vì list đối tượng Pydantic để tương thích với tests
            return results

    @staticmethod
    def _list_snippets_tx(tx, skip: int, limit: int) -> List[dict]:
        query = (
            "MATCH (ks:KnowledgeSnippet) "
            "RETURN ks "
            "ORDER BY ks.createdAt DESC "
            "SKIP $skip LIMIT $limit"
        )
        result = tx.run(query, skip=skip, limit=limit)
        return [dict(record['ks']) for record in result]

    def update_snippet(self, snippet_id: str, snippet_update: KnowledgeSnippetUpdate) -> Optional[dict]:
        """Updates an existing snippet and increments its version."""
        update_data = snippet_update.model_dump(exclude_unset=True, by_alias=True)
        if not update_data:
            return self.get_snippet_by_id(snippet_id)

        update_data['updatedAt'] = datetime.utcnow()

        with self._get_db().session() as session:
            result = session.write_transaction(self._update_snippet_tx, snippet_id, update_data)
            # Trả về dict thay vì đối tượng Pydantic để tương thích với tests
            return result

    @staticmethod
    def _update_snippet_tx(tx, snippet_id: str, update_data: dict) -> dict:
        # Lấy snippet hiện tại, tăng version và tạo lịch sử
        get_query = "MATCH (ks:KnowledgeSnippet) WHERE ks.uid = $id OR ks.snippetId = $id RETURN ks"
        result = tx.run(get_query, id=snippet_id)
        record = result.single()
        
        if not record:
            return None
            
        current_snippet = dict(record['ks'])
        current_version = current_snippet.get('version', 1)
        
        # Cập nhật version và updatedAt
        update_data['version'] = current_version + 1
        update_data['updatedAt'] = datetime.utcnow()
        
        # Xây dựng câu lệnh Cypher
        set_clauses = []
        for key, value in update_data.items():
            if value is not None:
                # Xử lý đặc biệt cho datetime
                if isinstance(value, datetime):
                    set_clauses.append(f"ks.{key} = datetime($params.{key})")
                else:
                    set_clauses.append(f"ks.{key} = $params.{key}")
        
        if not set_clauses:
            return current_snippet  # Không có gì để cập nhật
        
        update_query = (
            "MATCH (ks:KnowledgeSnippet) WHERE ks.uid = $id OR ks.snippetId = $id "
            f"SET {', '.join(set_clauses)} "
            "RETURN ks"
        )
        
        result = tx.run(update_query, id=snippet_id, params=update_data)
        record = result.single()
        return dict(record['ks']) if record and record['ks'] else None

    def delete_snippet(self, snippet_id: str) -> bool:
        """Deletes a snippet by its ID."""
        with self._get_db().session() as session:
            result = session.write_transaction(self._delete_snippet_tx, snippet_id)
            return result

    @staticmethod
    def _delete_snippet_tx(tx, snippet_id: str) -> bool:
        query = (
            "MATCH (ks:KnowledgeSnippet) "
            "WHERE ks.uid = $id OR ks.snippetId = $id "
            "DETACH DELETE ks "
            "RETURN count(*) as deleted"
        )
        result = tx.run(query, id=snippet_id)
        record = result.single()
        return record and record['deleted'] > 0

# Singleton instance of the service
knowledge_snippet_service = KnowledgeSnippetService()
