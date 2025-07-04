import uuid
from neo4j import Driver
from typing import List, Optional
from datetime import datetime

from trm_api.db.session import get_driver
from trm_api.models.team import Team, TeamCreate, TeamUpdate, TeamInDB
from trm_api.services.utils import process_record, process_records, process_relationship_record
from trm_api.models.relationships import Relationship

class TeamService:
    """
    Service layer for handling business logic related to Teams.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    def create_team(self, team_create: TeamCreate) -> Team:
        """Creates a new Team node."""
        params = team_create.model_dump()
        params["teamId"] = str(uuid.uuid4())
        now = datetime.utcnow()
        params["createdAt"] = now
        params["updatedAt"] = now

        with self._get_db().session() as session:
            result = session.execute_write(self._create_team_tx, params)
            return Team(**result) if result else None

    @staticmethod
    def _create_team_tx(tx, params: dict) -> dict:
        query = (
            "CREATE (t:Team { "
            "  teamId: $teamId, "
            "  name: $name, "
            "  description: $description, "
            "  createdAt: datetime($createdAt), "
            "  updatedAt: datetime($updatedAt) "
            "}) "
            "RETURN t"
        )
        result = tx.run(query, params)
        record = result.single()
        return process_record(record) if record else None

    def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """Retrieves a single team by its unique ID."""
        with self._get_db().session() as session:
            result = session.execute_read(self._get_team_by_id_tx, team_id)
            return Team(**result) if result else None

    @staticmethod
    def _get_team_by_id_tx(tx, team_id: str) -> Optional[dict]:
        query = "MATCH (t:Team {teamId: $teamId}) RETURN t"
        result = tx.run(query, teamId=team_id)
        record = result.single()
        return process_record(record)

    def list_teams(self, skip: int = 0, limit: int = 100) -> List[Team]:
        """Retrieves a list of teams with pagination."""
        with self._get_db().session() as session:
            results = session.execute_read(self._list_teams_tx, skip, limit)
            return [Team(**result) for result in results if result]

    @staticmethod
    def _list_teams_tx(tx, skip: int, limit: int) -> List[dict]:
        query = (
            "MATCH (t:Team) "
            "RETURN t "
            "ORDER BY t.name ASC "
            "SKIP $skip LIMIT $limit"
        )
        result = tx.run(query, skip=skip, limit=limit)
        return [process_record(record) for record in result]

    def update_team(self, team_id: str, team_update: TeamUpdate) -> Optional[Team]:
        """Updates an existing team."""
        update_data = team_update.model_dump(exclude_unset=True, by_alias=True)
        if not update_data:
            return self.get_team_by_id(team_id)

        update_data['updatedAt'] = datetime.utcnow()

        with self._get_db().session() as session:
            result = session.execute_write(self._update_team_tx, team_id, update_data)
            return Team(**result) if result else None

    @staticmethod
    def _update_team_tx(tx, team_id: str, update_data: dict) -> Optional[dict]:
        set_clauses = [f"t.{key} = ${key}" for key in update_data.keys()]
        if 'updatedAt' in update_data:
            set_clauses.remove('t.updatedAt = $updatedAt')
            set_clauses.append('t.updatedAt = datetime($updatedAt)')

        query = (
            f"MATCH (t:Team {{teamId: $teamId}}) "
            f"SET {', '.join(set_clauses)} "
            "RETURN t"
        )
        params = {'teamId': team_id, **update_data}
        result = tx.run(query, params)
        record = result.single()
        return process_record(record)

    def delete_team(self, team_id: str) -> bool:
        """Deletes a team by its ID."""
        with self._get_db().session() as session:
            result = session.execute_write(self._delete_team_tx, team_id)
            return result

    @staticmethod
    def _delete_team_tx(tx, team_id: str) -> bool:
        query = "MATCH (t:Team {teamId: $teamId}) DETACH DELETE t"
        result = tx.run(query, teamId=team_id)
        summary = result.consume()
        return summary.counters.nodes_deleted > 0

    def add_member_to_team(self, team_id: str, user_id: str) -> Optional[Relationship]:
        """Adds a user to a team, creating a HAS_MEMBER relationship."""
        with self._get_db().session() as session:
            result = session.execute_write(self._add_member_to_team_tx, team_id, user_id)
            return Relationship(**result) if result else None

    @staticmethod
    def _add_member_to_team_tx(tx, team_id: str, user_id: str) -> Optional[dict]:
        query = (
            "MATCH (t:Team {teamId: $teamId}) "
            "MATCH (u:User {userId: $userId}) "
            "MERGE (t)-[r:HAS_MEMBER]->(u) "
            "ON CREATE SET r.createdAt = datetime() "
            "RETURN "
            "    t.teamId AS source_id, "
            "    labels(t)[0] AS source_type, "
            "    u.userId AS target_id, "
            "    labels(u)[0] AS target_type, "
            "    type(r) AS type, "
            "    r.createdAt as createdAt"
        )
        result = tx.run(query, teamId=team_id, userId=user_id)
        record = result.single()
        return process_relationship_record(record)

# Singleton instance of the service
team_service = TeamService()
