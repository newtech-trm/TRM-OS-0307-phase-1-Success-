from typing import Optional, List, Tuple, Dict, Any
from neomodel import db
import uuid
import math
from datetime import datetime
from trm_api.graph_models.project import Project as GraphProject
from trm_api.graph_models.tension import Tension as GraphTension
from trm_api.graph_models.task import Task as GraphTask
from trm_api.graph_models.resource import Resource as GraphResource
from trm_api.graph_models.agent import Agent as GraphAgent
from trm_api.graph_models.knowledge_asset import KnowledgeAsset as GraphKnowledgeAsset
from trm_api.models.project import ProjectCreate, ProjectUpdate, ProjectDetail # This is the Pydantic model for API data

class ProjectRepository:
    async def create_project(self, project_data: ProjectCreate) -> GraphProject:
        """
        Creates a new project with extended properties asynchronously.
        """
        # Extract core and extended properties from project_data
        # Use getattr to safely get optional properties
        project = GraphProject(
            title=project_data.title,
            description=project_data.description,
            status=project_data.status,
            # Extended properties
            goal=getattr(project_data, 'goal', None),
            scope=getattr(project_data, 'scope', None),
            priority=getattr(project_data, 'priority', 3),
            project_type=getattr(project_data, 'project_type', None),
            tags=getattr(project_data, 'tags', []),
            start_date=getattr(project_data, 'start_date', None),
            target_end_date=getattr(project_data, 'target_end_date', None),
            actual_end_date=getattr(project_data, 'actual_end_date', None),
            health=getattr(project_data, 'health', 'normal'),
            metrics=getattr(project_data, 'metrics', {}),
            is_strategic=getattr(project_data, 'is_strategic', False)
        ).save()
        
        # If this is a subproject, create relationship to parent project
        if hasattr(project_data, 'parent_project_id') and project_data.parent_project_id:
            parent_project = await self.get_project_by_id(project_data.parent_project_id)
            if parent_project:
                project.parent_project.connect(parent_project)
        
        return project

    async def get_project_by_id(self, project_id: str) -> Optional[GraphProject]:
        """
        Retrieves a project by its unique ID asynchronously.
        """
        try:
            return GraphProject.nodes.get(uid=project_id)
        except GraphProject.DoesNotExist:
            return None

    def list_projects(self, skip: int = 0, limit: int = 100) -> List[GraphProject]:
        """
        Retrieves a list of all projects with pagination.
        """
        all_projects = GraphProject.nodes.all().order_by('title')  # Add order_by before pagination
        return list(all_projects[skip:skip + limit])  # Convert to list before returning
        
    async def get_paginated_projects(self, page: int = 1, page_size: int = 10) -> Tuple[List[GraphProject], int, int]:
        """
        Gets paginated projects with total count and page count.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (projects, total_count, page_count)
        """
        # Get all projects as a list
        all_projects = list(GraphProject.nodes.all())
        
        # Sort projects manually by title
        sorted_projects = sorted(all_projects, key=lambda x: x.title if hasattr(x, 'title') and x.title else '')
        
        # Calculate pagination metadata
        total_count = len(sorted_projects)
        page_count = math.ceil(total_count / page_size)
        
        # Paginate projects
        start_idx = (page - 1) * page_size
        end_idx = page * page_size
        paginated_projects = sorted_projects[start_idx:end_idx] if start_idx < len(sorted_projects) else []
        
        return paginated_projects, total_count, page_count

    async def update_project(self, project_id: str, project_data: ProjectUpdate) -> Optional[GraphProject]:
        """
        Updates an existing project asynchronously.
        """
        try:
            project = GraphProject.nodes.get(uid=project_id)
            # Update only the fields that are provided in the update data
            update_dict = project_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(project, field, value)
            project.save()
            return project
        except GraphProject.DoesNotExist:
            return None

    async def delete_project(self, project_id: str) -> bool:
        """
        Deletes a project by ID asynchronously.
        """
        try:
            project = GraphProject.nodes.get(uid=project_id)
            # Delete all relationships first
            db.cypher_query(f"MATCH (p:Project {{uid: '{project_id}'}}) DETACH DELETE p")
            return True
        except GraphProject.DoesNotExist:
            return False
        
    @db.transaction
    async def add_tension_to_resolve(self, project_uid: str, tension_uid: str, 
                           resolution_status: str = "Proposed", 
                           resolution_approach: Optional[str] = None,
                           expected_outcome: Optional[str] = None,
                           alignment_score: Optional[float] = None,
                           priority: Optional[str] = None,
                           start_date: Optional[datetime] = None,
                           target_resolution_date: Optional[datetime] = None,
                           actual_resolution_date: Optional[datetime] = None,
                           notes: Optional[str] = None) -> Optional[Tuple[GraphProject, GraphTension]]:
        """
        Establishes a RESOLVES_TENSION relationship from a Project to a Tension
        with all required properties according to the TRM Ontology V3.2.
        
        Args:
            project_uid: UID of the project
            tension_uid: UID of the tension
            resolution_status: Status of the resolution (e.g. 'Proposed', 'ResolutionInProgress')
            resolution_approach: Description of the approach to resolve the tension
            expected_outcome: Expected outcome after tension resolution
            alignment_score: Score (0.0-1.0) evaluating how well the project fits for resolving this tension
            priority: Priority level ('Critical', 'High', 'Medium', 'Low', 'Informational')
            start_date: Date when project started resolving this tension
            target_resolution_date: Target date for tension resolution
            actual_resolution_date: Actual date when tension was resolved
            notes: Additional notes about this relationship
        
        Returns:
            Tuple of (project, tension) if successful, None otherwise
        """
        import uuid
        from datetime import datetime
        
        # 1. Get both the project and tension nodes
        project = await self.get_project_by_id(project_uid)
        if not project:
            return None
            
        try:
            tension = GraphTension.nodes.get(uid=tension_uid)
        except GraphTension.DoesNotExist:
            return None
        
        # 2. Create the RESOLVES_TENSION relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'resolutionStatus': resolution_status,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now()
        }
        
        # Add optional properties if provided
        if resolution_approach:
            relationship_props['resolutionApproach'] = resolution_approach
        if expected_outcome:
            relationship_props['expectedOutcome'] = expected_outcome
        if alignment_score is not None:
            relationship_props['alignmentScore'] = alignment_score
        if priority:
            relationship_props['priority'] = priority
        if start_date:
            relationship_props['startDate'] = start_date
        if target_resolution_date:
            relationship_props['targetResolutionDate'] = target_resolution_date
        if actual_resolution_date:
            relationship_props['actualResolutionDate'] = actual_resolution_date
        if notes:
            relationship_props['notes'] = notes
        
        # Connect with relationship properties
        project.resolves_tensions.connect(tension, relationship_props)
        
        return (project, tension)
        
    async def get_tensions_resolved_by_project(self, project_uid: str, skip: int = 0, limit: int = 100) -> List[GraphTension]:
        """
        Retrieves all Tensions that are being resolved by a specific Project.
        """
        project = await self.get_project_by_id(project_uid)
        if not project:
            return []
            
        # Get all tensions connected with RESOLVES_TENSION relationship
        return list(project.resolves_tensions.all()[skip:skip+limit])
        
    async def get_paginated_tensions_by_project(self, project_uid: str, page: int = 1, page_size: int = 10) -> Tuple[List[GraphTension], int, int]:
        """
        Retrieves a paginated list of tensions that are resolved by a specific project.
        
        Args:
            project_uid: UID of the project
            page: The page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (tensions, total_count, page_count)
        """
        from trm_api.repositories.pagination_helper import PaginationHelper
        
        project = await self.get_project_by_id(project_uid)
        if not project:
            return [], 0, 0
            
        return PaginationHelper.paginate_relationship(project.resolves_tensions, page, page_size)
        
    @db.transaction
    def remove_tension_from_project(self, project_uid: str, tension_uid: str) -> bool:
        """
        Removes the RESOLVES_TENSION relationship between a Project and a Tension.
        
        Returns True if disconnection was successful, False otherwise.
        """
        # 1. Get both the project and tension nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            tension = GraphTension.nodes.get(uid=tension_uid)
        except GraphTension.DoesNotExist:
            return False
            
        # 2. Remove the relationship
        project.resolves_tensions.disconnect(tension)
        
        return True
        
    @db.transaction
    def add_task_to_project(self, project_uid: str, task_uid: str, 
                            task_order: int = 0,
                            is_required: bool = True,
                            criticality: int = 3,
                            depends_on: str = None,
                            milestone: str = None,
                            added_by: str = None,
                            notes: str = None) -> Optional[Tuple[GraphProject, GraphTask]]:
        """
        Establishes an IS_PART_OF_PROJECT (HAS_TASK) relationship from a Project to a Task
        with all required properties according to the TRM Ontology V3.2.
        
        Args:
            project_uid: UID of the project
            task_uid: UID of the task
            task_order: Order/position of the task in the project (0 = first)
            is_required: Whether task is required for project completion
            criticality: Criticality level (1-5)
                1: Critical
                2: High
                3: Medium
                4: Low
                5: Optional
            depends_on: UID of task that this task depends on
            milestone: Milestone this task contributes to
            added_by: UID of user who added this task to the project
            notes: Additional notes about this relationship
            
        Returns:
            Tuple of (project, task) if successful, None otherwise
        """
        # 1. Get both the project and task nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return None
            
        try:
            task = GraphTask.nodes.get(uid=task_uid)
        except GraphTask.DoesNotExist:
            return None
        
        # 2. Create the IS_PART_OF_PROJECT relationship with all properties
        relationship_props = {
            'relationshipId': str(uuid.uuid4()),
            'taskOrder': task_order,
            'creationDate': datetime.now(),
            'lastModifiedDate': datetime.now(),
            'isRequired': is_required,
            'criticality': criticality
        }
        
        # Add optional properties if provided
        if depends_on:
            relationship_props['dependsOn'] = depends_on
        if milestone:
            relationship_props['milestone'] = milestone
        if added_by:
            relationship_props['addedBy'] = added_by
        if notes:
            relationship_props['notes'] = notes
        
        # Connect with relationship properties
        project.tasks.connect(task, relationship_props)
        
        return (project, task)
        
    def get_project_tasks(self, project_uid: str, skip: int = 0, limit: int = 100) -> List[GraphTask]:
        """
        Retrieves all Tasks that are part of a specific Project.
        
        Args:
            project_uid: UID of the project
            skip: Number of items to skip (pagination)
            limit: Maximum number of items to return (pagination)
            
        Returns:
            List of Task nodes
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        # Get all tasks connected with HAS_TASK relationship
        return list(project.tasks.all()[skip:skip+limit])
        
    def get_paginated_tasks_by_project(self, project_uid: str, page: int = 1, page_size: int = 10) -> Tuple[List[GraphTask], int, int]:
        """
        Retrieves a paginated list of tasks that are part of a specific project.
        
        Args:
            project_uid: UID of the project
            page: The page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (tasks, total_count, page_count)
        """
        from trm_api.repositories.pagination_helper import PaginationHelper
        
        project = self.get_project_by_uid(project_uid)
        if not project:
            return [], 0, 0
            
        return PaginationHelper.paginate_relationship(project.tasks, page, page_size)
        
    def get_project_tasks_with_relationships(self, project_uid: str) -> List[Dict[str, Any]]:
        """
        Retrieves all Tasks that are part of a specific Project,
        including the relationship properties according to the ontology V3.2.
        
        Args:
            project_uid: UID of the project
            
        Returns:
            List of dictionaries with task data and relationship properties
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        results = []
        # Get all task relationships
        relationships = project.tasks.all_relationships()
        
        for rel in relationships:
            # Get task node data
            task = rel.end_node()
            
            # Combine task data with relationship properties
            task_data = {
                'task': task.model_dump(),
                'relationship': {
                    'relationshipId': rel.relationshipId,
                    'taskOrder': rel.taskOrder,
                    'creationDate': rel.creationDate,
                    'lastModifiedDate': rel.lastModifiedDate,
                    'isRequired': rel.isRequired,
                    'criticality': rel.criticality,
                    'dependsOn': getattr(rel, 'dependsOn', None),
                    'milestone': getattr(rel, 'milestone', None),
                    'addedBy': getattr(rel, 'addedBy', None),
                    'notes': getattr(rel, 'notes', None)
                }
            }
            results.append(task_data)
        
        # Sort by taskOrder
        results.sort(key=lambda x: x['relationship']['taskOrder'])
        
        return results
        
    @db.transaction
    def update_task_project_relationship(self, project_uid: str, task_uid: str,
                                         task_order: int = None,
                                         is_required: bool = None,
                                         criticality: int = None,
                                         depends_on: str = None,
                                         milestone: str = None,
                                         notes: str = None) -> bool:
        """
        Updates the relationship properties between a Project and a Task
        according to the TRM Ontology V3.2.
        
        Returns True if update was successful, False otherwise.
        """
        # 1. Get both the project and task nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            task = GraphTask.nodes.get(uid=task_uid)
        except GraphTask.DoesNotExist:
            return False
            
        # Check if relationship exists
        if not project.tasks.is_connected(task):
            return False
            
        # 2. Get the relationship
        rel = project.tasks.relationship(task)
        
        # 3. Update the properties
        if task_order is not None:
            rel.taskOrder = task_order
        if is_required is not None:
            rel.isRequired = is_required
        if criticality is not None:
            rel.criticality = criticality
        if depends_on is not None:
            rel.dependsOn = depends_on
        if milestone is not None:
            rel.milestone = milestone
        if notes is not None:
            rel.notes = notes
            
        rel.lastModifiedDate = datetime.now()
        rel.save()
        
        return True
        
    @db.transaction
    def remove_task_from_project(self, project_uid: str, task_uid: str) -> bool:
        """
        Removes the IS_PART_OF_PROJECT relationship between a Project and a Task.
        
        Returns True if disconnection was successful, False otherwise.
        """
        # 1. Get both the project and task nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            task = GraphTask.nodes.get(uid=task_uid)
        except GraphTask.DoesNotExist:
            return False
            
        # 2. Remove the relationship
        project.tasks.disconnect(task)
        
        return True
        
    # --- Resource Management Methods ---
    
    @db.transaction
    def assign_resource_to_project(self, project_uid: str, resource_uid: str,
                            allocation_percentage: int = 100,
                            assignment_type: str = 'full',
                            expected_end_date = None,
                            assignment_status: str = 'active',
                            notes: str = None,
                            assigned_by: str = None) -> Optional[Tuple[GraphProject, GraphResource]]:
        """
        Establishes an ASSIGNED_TO_PROJECT relationship from a Resource to a Project
        with all required properties according to the TRM Ontology V3.2.
        
        Args:
            project_uid: UID of the project
            resource_uid: UID of the resource
            allocation_percentage: Percentage of resource allocated to this project (0-100)
            assignment_type: Type of assignment (full, partial, on-demand)
            expected_end_date: When the resource allocation is expected to end
            assignment_status: Status of the assignment (active, completed, on-hold, cancelled)
            notes: Notes about this resource assignment
            assigned_by: UID of the Agent who assigned this resource
            
        Returns:
            Tuple of (Project, Resource) if successful, None otherwise
        """
        # 1. Get both the project and resource nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return None
            
        try:
            resource = GraphResource.nodes.get(uid=resource_uid)
        except GraphResource.DoesNotExist:
            return None
            
        # 2. Create the relationship with properties
        rel = resource.assigned_to_projects.connect(project)
        rel.allocation_percentage = allocation_percentage
        rel.assigned_at = datetime.now()
        if expected_end_date:
            rel.expected_end_date = expected_end_date
        rel.assignment_type = assignment_type
        rel.assignment_status = assignment_status
        if notes:
            rel.notes = notes
        if assigned_by:
            rel.assigned_by = assigned_by
        rel.save()
        
        return (project, resource)
        
    def get_project_resources(self, project_uid: str, skip: int = 0, limit: int = 100) -> List[GraphResource]:
        """
        Retrieves all Resources that are assigned to a specific Project.
        
        Args:
            project_uid: UID of the project
            skip: Number of items to skip (pagination)
            limit: Maximum number of items to return (pagination)
            
        Returns:
            List of Resource nodes
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        # Fetch resources assigned to this project
        # The relationship is from Resource to Project (Resource -[ASSIGNED_TO_PROJECT]-> Project)
        query = f"""
        MATCH (r:Resource)-[:ASSIGNED_TO_PROJECT]->(p:Project {{uid: $uid}})
        RETURN r
        SKIP {skip}
        LIMIT {limit}
        """
        
        results, _ = db.cypher_query(query, {'uid': project_uid})
        resources = [GraphResource.inflate(row[0]) for row in results]
        
        return resources
        
    def get_paginated_resources_by_project(self, project_uid: str, page: int = 1, page_size: int = 10) -> Tuple[List[GraphResource], int, int]:
        """
        Retrieves a paginated list of resources that are assigned to a specific project.
        
        Args:
            project_uid: UID of the project
            page: The page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (resources, total_count, page_count)
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return [], 0, 0
            
        # First count total resources
        count_query = """
        MATCH (r:Resource)-[:ASSIGNED_TO_PROJECT]->(p:Project {uid: $uid})
        RETURN COUNT(r) as count
        """
        count_results, _ = db.cypher_query(count_query, {'uid': project_uid})
        total_count = count_results[0][0]
        
        # Calculate page count
        page_count = (total_count + page_size - 1) // page_size if total_count > 0 else 0
        
        # Then get paginated resources
        skip = (page - 1) * page_size
        resources = self.get_project_resources(project_uid, skip=skip, limit=page_size)
        
        return resources, total_count, page_count
        
    def get_project_resources_with_relationships(self, project_uid: str) -> List[Dict[str, Any]]:
        """
        Retrieves all Resources that are assigned to a specific Project,
        including the relationship properties according to the ontology V3.2.
        
        Args:
            project_uid: UID of the project
            
        Returns:
            List of dictionaries with resource data and relationship properties
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        # The relationship is from Resource to Project (Resource -[ASSIGNED_TO_PROJECT]-> Project)
        query = """
        MATCH (r:Resource)-[rel:ASSIGNED_TO_PROJECT]->(p:Project {uid: $uid})
        RETURN r, rel
        """
        
        results, _ = db.cypher_query(query, {'uid': project_uid})
        
        resource_list = []
        for row in results:
            resource = GraphResource.inflate(row[0])
            rel = row[1]  # This is the relationship data
            
            resource_data = {
                'resource': resource.model_dump(),
                'relationship': {
                    'allocation_percentage': rel.allocation_percentage if hasattr(rel, 'allocation_percentage') else 100,
                    'assigned_at': rel.assigned_at if hasattr(rel, 'assigned_at') else None,
                    'expected_end_date': rel.expected_end_date if hasattr(rel, 'expected_end_date') else None,
                    'actual_end_date': rel.actual_end_date if hasattr(rel, 'actual_end_date') else None,
                    'assignment_type': rel.assignment_type if hasattr(rel, 'assignment_type') else 'full',
                    'assignment_status': rel.assignment_status if hasattr(rel, 'assignment_status') else 'active',
                    'notes': rel.notes if hasattr(rel, 'notes') else None,
                    'assigned_by': rel.assigned_by if hasattr(rel, 'assigned_by') else None
                }
            }
            resource_list.append(resource_data)
        
        return resource_list
        
    @db.transaction
    def update_resource_project_relationship(self, project_uid: str, resource_uid: str,
                                           allocation_percentage: int = None,
                                           expected_end_date = None,
                                           actual_end_date = None,
                                           assignment_type: str = None,
                                           assignment_status: str = None,
                                           notes: str = None) -> bool:
        """
        Updates the relationship properties between a Resource and a Project
        according to the TRM Ontology V3.2.
        
        Returns True if update was successful, False otherwise.
        """
        # 1. Get both the project and resource nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            resource = GraphResource.nodes.get(uid=resource_uid)
        except GraphResource.DoesNotExist:
            return False
            
        # Check if relationship exists
        # The relationship is from Resource to Project (Resource -[ASSIGNED_TO_PROJECT]-> Project)
        if not resource.assigned_to_projects.is_connected(project):
            return False
            
        # 2. Get the relationship
        rel = resource.assigned_to_projects.relationship(project)
        
        # 3. Update the properties
        if allocation_percentage is not None:
            rel.allocation_percentage = allocation_percentage
        if expected_end_date is not None:
            rel.expected_end_date = expected_end_date
        if actual_end_date is not None:
            rel.actual_end_date = actual_end_date
        if assignment_type is not None:
            rel.assignment_type = assignment_type
        if assignment_status is not None:
            rel.assignment_status = assignment_status
        if notes is not None:
            rel.notes = notes
            
        rel.save()
        
        return True
        
    @db.transaction
    def unassign_resource_from_project(self, project_uid: str, resource_uid: str) -> bool:
        """
        Removes the ASSIGNED_TO_PROJECT relationship between a Resource and a Project.
        
        Returns True if disconnection was successful, False otherwise.
        """
        # 1. Get both the project and resource nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            resource = GraphResource.nodes.get(uid=resource_uid)
        except GraphResource.DoesNotExist:
            return False
            
        # 2. Check if relationship exists and remove it
        # The relationship is from Resource to Project (Resource -[ASSIGNED_TO_PROJECT]-> Project)
        if resource.assigned_to_projects.is_connected(project):
            resource.assigned_to_projects.disconnect(project)
            return True
        else:
            return False
    
    # --- Project Manager and Agent Methods ---
    
    @db.transaction
    def assign_manager_to_project(self, project_uid: str, agent_uid: str,
                                  role: str = 'project_manager',
                                  responsibility_level: str = 'primary',
                                  appointed_at = None,
                                  notes: str = None) -> Optional[Tuple[GraphProject, GraphAgent]]:
        """
        Establishes a MANAGES_PROJECT relationship from an Agent to a Project
        according to the TRM Ontology V3.2.
        
        Args:
            project_uid: UID of the project
            agent_uid: UID of the agent (user or internal agent)
            role: Role of the agent in the project
            responsibility_level: Level of responsibility (primary, secondary, support)
            appointed_at: When the agent was appointed to manage the project
            notes: Notes about this management relationship
            
        Returns:
            Tuple of (Project, Agent) if successful, None otherwise
        """
        # 1. Get both the project and agent nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return None
            
        try:
            agent = GraphAgent.nodes.get(uid=agent_uid)
        except GraphAgent.DoesNotExist:
            return None
            
        # 2. Create the relationship with properties
        rel = agent.manages_projects.connect(project)
        rel.role = role
        rel.responsibility_level = responsibility_level
        rel.appointed_at = appointed_at or datetime.now()
        if notes:
            rel.notes = notes
        rel.save()
        
        return (project, agent)
    
    def get_project_managers(self, project_uid: str) -> List[GraphAgent]:
        """
        Retrieves all Agents that manage a specific Project.
        
        Args:
            project_uid: UID of the project
            
        Returns:
            List of Agent nodes
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        # Fetch agents managing this project
        # The relationship is from Agent to Project (Agent -[MANAGES_PROJECT]-> Project)
        query = """
        MATCH (a:Agent)-[:MANAGES_PROJECT]->(p:Project {uid: $uid})
        RETURN a
        """
        
        results, _ = db.cypher_query(query, {'uid': project_uid})
        managers = [GraphAgent.inflate(row[0]) for row in results]
        
        return managers
    
    def get_project_managers_with_relationships(self, project_uid: str) -> List[Dict[str, Any]]:
        """
        Retrieves all Agents that manage a specific Project,
        including the relationship properties according to the ontology V3.2.
        
        Args:
            project_uid: UID of the project
            
        Returns:
            List of dictionaries with agent data and relationship properties
        """
        project = self.get_project_by_uid(project_uid)
        if not project:
            return []
            
        # The relationship is from Agent to Project (Agent -[MANAGES_PROJECT]-> Project)
        query = """
        MATCH (a:Agent)-[rel:MANAGES_PROJECT]->(p:Project {uid: $uid})
        RETURN a, rel
        """
        
        results, _ = db.cypher_query(query, {'uid': project_uid})
        
        manager_list = []
        for row in results:
            agent = GraphAgent.inflate(row[0])
            rel = row[1]  # This is the relationship data
            
            manager_data = {
                'agent': agent.model_dump(),
                'relationship': {
                    'role': rel.role if hasattr(rel, 'role') else 'project_manager',
                    'responsibility_level': rel.responsibility_level if hasattr(rel, 'responsibility_level') else 'primary',
                    'appointed_at': rel.appointed_at if hasattr(rel, 'appointed_at') else None,
                    'notes': rel.notes if hasattr(rel, 'notes') else None
                }
            }
            manager_list.append(manager_data)
        
        return manager_list
    
    @db.transaction
    def update_manager_project_relationship(self, project_uid: str, agent_uid: str,
                                          role: str = None,
                                          responsibility_level: str = None,
                                          notes: str = None) -> bool:
        """
        Updates the relationship properties between an Agent and a Project
        according to the TRM Ontology V3.2.
        
        Returns True if update was successful, False otherwise.
        """
        # 1. Get both the project and agent nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            agent = GraphAgent.nodes.get(uid=agent_uid)
        except GraphAgent.DoesNotExist:
            return False
            
        # Check if relationship exists
        # The relationship is from Agent to Project (Agent -[MANAGES_PROJECT]-> Project)
        if not agent.manages_projects.is_connected(project):
            return False
            
        # 2. Get the relationship
        rel = agent.manages_projects.relationship(project)
        
        # 3. Update the properties
        if role is not None:
            rel.role = role
        if responsibility_level is not None:
            rel.responsibility_level = responsibility_level
        if notes is not None:
            rel.notes = notes
            
        rel.save()
        
        return True
    
    @db.transaction
    def remove_manager_from_project(self, project_uid: str, agent_uid: str) -> bool:
        """
        Removes the MANAGES_PROJECT relationship between an Agent and a Project.
        
        Returns True if disconnection was successful, False otherwise.
        """
        # 1. Get both the project and agent nodes
        project = self.get_project_by_uid(project_uid)
        if not project:
            return False
            
        try:
            agent = GraphAgent.nodes.get(uid=agent_uid)
        except GraphAgent.DoesNotExist:
            return False
            
        # 2. Check if relationship exists and remove it
        # The relationship is from Agent to Project (Agent -[MANAGES_PROJECT]-> Project)
        if agent.manages_projects.is_connected(project):
            agent.manages_projects.disconnect(project)
            return True
        else:
            return False
