from neo4j import Driver
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException
from uuid import uuid4

from trm_api.db.session import get_driver
from trm_api.models.agent import Agent, AgentCreate, AgentUpdate, AgentInDB
import logging
import asyncio

logger = logging.getLogger(__name__)

class AgentService:
    """
    Service layer for handling business logic related to Agents.
    """

    def _get_db(self) -> Driver:
        return get_driver()

    async def create_agent(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent"""
        agent_id = str(uuid4())
        agent_type = parameters.get("agent_type", "CODE_GENERATOR")
        
        agent = {
            "id": agent_id,
            "type": agent_type,
            "name": f"Agent {agent_type}",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "capabilities": self._get_agent_capabilities(agent_type)
        }
        
        async with self._get_db().driver.session() as session:
            await session.execute_write(self._create_agent_tx, agent_id, agent)
        
        return agent

    @staticmethod
    def _create_agent_tx(tx, agent_id: str, agent: dict) -> Optional[dict]:
        # params includes aliased keys like agentId, agentType, creationDate, etc.
        query = (
            "CREATE (a:Agent { "
            "  uid: $agentId, "                 # Neo4j 'uid' from params['agentId']
            "  name: $name, "
            "  agent_type: $agentType, "       # Neo4j 'agent_type' from params['agentType']
            "  purpose: $purpose, "
            "  description: $description, "
            "  status: $status, "
            "  capabilities: $capabilities, "
            "  job_title: $jobTitle, "
            "  department: $department, "
            "  is_founder: $isFounder, "
            "  founder_recognition_authority: $founderRecognitionAuthority, "
            "  contact_info: $contactInfo, "
            "  creation_date: datetime($creationDate), "          # Neo4j 'creation_date'
            "  last_modified_date: datetime($lastModifiedDate) "  # Neo4j 'last_modified_date'
            # 'purpose' is in Pydantic model but not in Agent graph_model, so not persisted here.
            "}) "
            "RETURN "
            "  a.uid AS agentId, "
            "  a.name AS name, "
            "  a.agent_type AS agentType, "
            "  a.purpose AS purpose, "
            "  a.description AS description, "
            "  a.status AS status, "
            "  a.capabilities AS capabilities, "
            "  a.job_title AS jobTitle, "
            "  a.department AS department, "
            "  a.is_founder AS isFounder, "
            "  a.founder_recognition_authority AS founderRecognitionAuthority, "
            "  a.contact_info AS contactInfo, "
            "  a.creation_date AS creationDate, "
            "  a.last_modified_date AS lastModifiedDate"
            # 'purpose' from Pydantic is not returned as it's not stored on the node
            # tool_ids are not directly on the Agent node in graph_model, handle via relationships if needed
        )
        
        logger.debug(f"Cypher query for CREATE Agent: {query}")  # For debugging
        logger.debug(f"Cypher params for CREATE Agent: {agent}")  # For debugging

        result = tx.run(query, agentId=agent_id, name=agent['name'], agentType=agent['type'], purpose=agent['purpose'], description=agent['description'], status=agent['status'], capabilities=agent['capabilities'], jobTitle=agent['job_title'], department=agent['department'], isFounder=agent['is_founder'], founderRecognitionAuthority=agent['founder_recognition_authority'], contactInfo=agent['contact_info'], creationDate=agent['created_at'], lastModifiedDate=agent['created_at'])
        record = result.single()
        
        if record:
            logger.debug(f"Record from DB after CREATE Agent: {dict(record)}")  # For debugging
            return dict(record)
        return None

    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        async with self._get_db().driver.session() as session:
            result_data = await session.execute_read(self._get_agent_by_id_tx, agent_id)
       
        if not result_data:
            return None
       
        # Convert neo4j.time.DateTime to python datetime
        if 'creationDate' in result_data and result_data['creationDate'] is not None:
            if hasattr(result_data['creationDate'], 'to_native'):
                result_data['creationDate'] = result_data['creationDate'].to_native()
        if 'lastModifiedDate' in result_data and result_data['lastModifiedDate'] is not None:
            if hasattr(result_data['lastModifiedDate'], 'to_native'):
                result_data['lastModifiedDate'] = result_data['lastModifiedDate'].to_native()
       
        return result_data

    @staticmethod
    def _get_agent_by_id_tx(tx, agent_id: str) -> Optional[dict]:
        query = (
            "MATCH (a:Agent {uid: $agentId}) "
            "RETURN "
            "  a.uid AS agentId, "
            "  a.name AS name, "
            "  a.agent_type AS agentType, "
            "  a.purpose AS purpose, "
            "  a.description AS description, "
            "  a.status AS status, "
            "  a.capabilities AS capabilities, "
            "  a.job_title AS jobTitle, "
            "  a.department AS department, "
            "  a.is_founder AS isFounder, "
            "  a.founder_recognition_authority AS founderRecognitionAuthority, "
            "  a.contact_info AS contactInfo, "
            "  a.creation_date AS creationDate, "
            "  a.last_modified_date AS lastModifiedDate"
        )
        result = tx.run(query, agentId=agent_id)
        record = result.single()
        return dict(record) if record else None

    async def list_agents(self) -> list:
        """List all agents"""
        async with self._get_db().driver.session() as session:
            raw_results = await session.execute_read(self._list_agents_tx)
       
        processed_agents = []
        for agent_data in raw_results:
            # Convert neo4j.time.DateTime to python datetime
            if 'creationDate' in agent_data and agent_data['creationDate'] is not None:
                if hasattr(agent_data['creationDate'], 'to_native'):
                    agent_data['creationDate'] = agent_data['creationDate'].to_native()
            if 'lastModifiedDate' in agent_data and agent_data['lastModifiedDate'] is not None:
                if hasattr(agent_data['lastModifiedDate'], 'to_native'):
                    agent_data['lastModifiedDate'] = agent_data['lastModifiedDate'].to_native()
            processed_agents.append(agent_data)
        return processed_agents

    @staticmethod
    def _list_agents_tx(tx) -> List[dict]:
        query = (
            "MATCH (a:Agent) "
            "RETURN "
            "  a.uid AS agentId, "
            "  a.name AS name, "
            "  a.agent_type AS agentType, "
            "  a.purpose AS purpose, "
            "  a.description AS description, "
            "  a.status AS status, "
            "  a.capabilities AS capabilities, "
            "  a.job_title AS jobTitle, "
            "  a.department AS department, "
            "  a.is_founder AS isFounder, "
            "  a.founder_recognition_authority AS founderRecognitionAuthority, "
            "  a.contact_info AS contactInfo, "
            "  a.creation_date AS creationDate, "
            "  a.last_modified_date AS lastModifiedDate"
        )
        result = tx.run(query)
        return [dict(record) for record in result]

    async def update_agent(self, agent_id: str, agent_update: AgentUpdate) -> Optional[Agent]:
        """Updates an existing agent asynchronously."""
        update_data_from_request = agent_update.model_dump(exclude_unset=True, by_alias=True)

        if not update_data_from_request:
            pass 

        final_update_data = update_data_from_request.copy()
        final_update_data['updatedAt'] = datetime.utcnow()

        async with self._get_db().driver.session() as session:
            result_data = await session.execute_write(self._update_agent_tx, agent_id, final_update_data)
    
        if not result_data:
            return None

        if 'creationDate' in result_data and result_data['creationDate'] is not None:
            if hasattr(result_data['creationDate'], 'to_native'):
                result_data['creationDate'] = result_data['creationDate'].to_native()
        if 'lastModifiedDate' in result_data and result_data['lastModifiedDate'] is not None:
            if hasattr(result_data['lastModifiedDate'], 'to_native'): 
                result_data['lastModifiedDate'] = result_data['lastModifiedDate'].to_native()
    
        return Agent(**result_data)

    @staticmethod
    def _update_agent_tx(tx, agent_id: str, update_data: dict) -> Optional[dict]:
        set_clauses = []
        for key in update_data.keys():
            if key == 'updatedAt': 
                set_clauses.append(f"a.last_modified_date = datetime($updatedAt)")
            elif key != 'agentId': 
                 set_clauses.append(f"a.{key} = ${key}")

        if not set_clauses:
            # This case implies only agentId was in update_data, which shouldn't happen if we add 'updatedAt'
            # Or if update_data was empty except for agentId. If 'updatedAt' is always added, this path is less likely.
            # However, if it's possible that no valid fields to SET are generated, we might need to return early or handle.
            # For now, assume 'updatedAt' ensures at least one SET clause.
            pass

        query = (
            f"MATCH (a:Agent {{uid: $agentId}}) "
            f"SET {', '.join(set_clauses)} "
            "RETURN "
            "  a.uid AS agentId, "
            "  a.name AS name, "
            "  a.agent_type AS agentType, "
            "  a.purpose AS purpose, "
            "  a.description AS description, "
            "  a.status AS status, "
            "  a.capabilities AS capabilities, "
            "  a.job_title AS jobTitle, "
            "  a.department AS department, "
            "  a.is_founder AS isFounder, "
            "  a.founder_recognition_authority AS founderRecognitionAuthority, "
            "  a.contact_info AS contactInfo, "
            "  a.creation_date AS creationDate, "
            "  a.last_modified_date AS lastModifiedDate"
        )
        params = {'agentId': agent_id, **update_data}
        result = tx.run(query, params)
        record = result.single()
        return dict(record) if record else None

    async def delete_agent(self, agent_id: str) -> bool:
        """Deletes an agent by its ID asynchronously."""
        async with self._get_db().driver.session() as session:
            result = await session.execute_write(self._delete_agent_tx, agent_id)
            return result

    @staticmethod
    def _delete_agent_tx(tx, agent_id: str) -> bool:
        query = "MATCH (a:Agent {uid: $agentId}) DETACH DELETE a" # Changed to uid
        result = tx.run(query, agentId=agent_id)
        summary = result.consume()
        return summary.counters.nodes_deleted > 0

    def _get_agent_capabilities(self, agent_type: str) -> list:
        """Get capabilities for agent type"""
        capabilities_map = {
            "CODE_GENERATOR": ["code_generation", "debugging", "testing"],
            "RESEARCH": ["research", "analysis", "documentation"],
            "DATA_ANALYST": ["data_analysis", "visualization", "reporting"],
            "USER_INTERFACE": ["ui_design", "ux_optimization", "prototyping"],
            "INTEGRATION": ["api_integration", "system_connection", "workflow_automation"]
        }
        return capabilities_map.get(agent_type, ["general_assistance"])

# Singleton instance of the service
agent_service = AgentService()
