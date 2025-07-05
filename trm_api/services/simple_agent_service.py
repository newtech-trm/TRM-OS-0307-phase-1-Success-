from neo4j import Driver
from typing import List, Optional

from trm_api.db.session import get_driver

class SimpleAgentService:
    """
    Simple service layer for handling Agents using direct Cypher queries.
    Similar to KnowledgeSnippetService for better reliability.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def list_agents(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Retrieves a list of agents with pagination."""
        with self._get_db().session() as session:
            results = session.read_transaction(self._list_agents_tx, skip, limit)
            return results

    @staticmethod
    def _list_agents_tx(tx, skip: int, limit: int) -> List[dict]:
        query = (
            "MATCH (a:Agent) "
            "RETURN a "
            "ORDER BY a.creation_date DESC "
            "SKIP $skip LIMIT $limit"
        )
        result = tx.run(query, skip=skip, limit=limit)
        return [dict(record['a']) for record in result]

    def get_agent_by_uid(self, uid: str) -> Optional[dict]:
        """Retrieves a single agent by its unique ID."""
        with self._get_db().session() as session:
            result = session.read_transaction(self._get_agent_by_uid_tx, uid)
            return result

    @staticmethod
    def _get_agent_by_uid_tx(tx, uid: str) -> Optional[dict]:
        query = (
            "MATCH (a:Agent) "
            "WHERE a.uid = $uid "
            "RETURN a"
        )
        result = tx.run(query, uid=uid)
        record = result.single()
        return dict(record['a']) if record and record['a'] else None

    def count_agents(self) -> int:
        """Count total number of agents."""
        with self._get_db().session() as session:
            result = session.read_transaction(self._count_agents_tx)
            return result

    @staticmethod
    def _count_agents_tx(tx) -> int:
        query = "MATCH (a:Agent) RETURN count(a) as count"
        result = tx.run(query)
        record = result.single()
        return record['count'] if record else 0

# Singleton instance of the service
simple_agent_service = SimpleAgentService() 