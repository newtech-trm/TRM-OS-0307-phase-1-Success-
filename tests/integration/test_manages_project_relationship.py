"""
Comprehensive Integration Tests for ManagesProjectRel relationship.
Tests Agent/User -> Project management relationships với đầy đủ validation, performance và edge cases.
"""

import pytest
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from trm_api.main import app
from trm_api.graph_models.agent import Agent
from trm_api.graph_models.user import User
from trm_api.graph_models.project import Project
from trm_api.graph_models.manages_project import ManagesProjectRel


class TestManagesProjectRelCRUD:
    """Test basic CRUD operations cho ManagesProjectRel"""
    
    def setup_method(self):
        """Setup test data cho mỗi test"""
        self.test_client = TestClient(app)
        
        # Tạo test entities
        self.agent = Agent(
            name="Project Manager Agent",
            description="AI agent specialized in project management",
            agent_type="AIAgent",
            status="active"
        ).save()
        
        self.user = User(
            username=f"pm_user_{uuid.uuid4().hex[:8]}",
            email=f"pm_{uuid.uuid4().hex[:8]}@example.com",
            full_name="Project Manager User"
        ).save()
        
        self.project = Project(
            title=f"Test Project {uuid.uuid4().hex[:8]}",
            description="Test project for management relationships",
            status="planning"
        ).save()
        
        self.secondary_project = Project(
            title=f"Secondary Project {uuid.uuid4().hex[:8]}",
            description="Secondary test project",
            status="active"
        ).save()
    
    def teardown_method(self):
        """Cleanup sau mỗi test"""
        # Delete relationships first
        if hasattr(self, 'agent') and self.agent:
            for rel in self.agent.manages_projects.all():
                rel.delete()
            self.agent.delete()
            
        if hasattr(self, 'user') and self.user:
            for rel in self.user.manages_projects.all():
                rel.delete()
            self.user.delete()
            
        if hasattr(self, 'project') and self.project:
            self.project.delete()
            
        if hasattr(self, 'secondary_project') and self.secondary_project:
            self.secondary_project.delete()
    
    def test_agent_manages_project_creation(self):
        """Test Agent -> Project management relationship creation"""
        # Create management relationship
        relationship = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'project_manager',
                'context': 'Primary management responsibility',
                'notes': 'Lead PM for this strategic project',
                'is_primary': True
            }
        )
        
        # Verify relationship exists
        assert relationship is not None
        assert relationship.role == 'project_manager'
        assert relationship.context == 'Primary management responsibility'
        assert relationship.notes == 'Lead PM for this strategic project'
        assert relationship.is_primary == True
        assert relationship.assigned_at is not None
        
        # Verify from agent side
        managed_projects = self.agent.manages_projects.all()
        assert len(managed_projects) == 1
        assert managed_projects[0].title == self.project.title
        
        # Verify from project side
        managers = self.project.managed_by
        assert len(managers) == 1
        assert managers[0].name == self.agent.name
    
    def test_user_manages_project_creation(self):
        """Test User -> Project management relationship creation"""
        # Create management relationship
        relationship = self.user.manages_projects.connect(
            self.project,
            {
                'role': 'sponsor',
                'context': 'Executive sponsorship',
                'notes': 'Provides strategic oversight and funding approval',
                'is_primary': False
            }
        )
        
        # Verify relationship
        assert relationship.role == 'sponsor'
        assert relationship.context == 'Executive sponsorship'
        assert relationship.is_primary == False
        assert relationship.assigned_at is not None
        
        # Verify bidirectional access
        managed_projects = self.user.manages_projects.all()
        assert len(managed_projects) == 1
        assert managed_projects[0].title == self.project.title
    
    def test_multiple_projects_per_manager(self):
        """Test Agent quản lý nhiều projects"""
        # Create management relationships for multiple projects
        rel1 = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'notes': 'Primary project'
            }
        )
        
        rel2 = self.agent.manages_projects.connect(
            self.secondary_project,
            {
                'role': 'coordinator',
                'is_primary': False,
                'notes': 'Secondary coordination role'
            }
        )
        
        # Verify both relationships
        managed_projects = self.agent.manages_projects.all()
        assert len(managed_projects) == 2
        
        project_titles = [project.title for project in managed_projects]
        assert self.project.title in project_titles
        assert self.secondary_project.title in project_titles
        
        # Verify different roles
        rel1_retrieved = self.agent.manages_projects.relationship(self.project)
        rel2_retrieved = self.agent.manages_projects.relationship(self.secondary_project)
        
        assert rel1_retrieved.role == 'project_manager'
        assert rel1_retrieved.is_primary == True
        assert rel2_retrieved.role == 'coordinator'
        assert rel2_retrieved.is_primary == False
    
    def test_multiple_managers_per_project(self):
        """Test Project có nhiều managers (Agent + User)"""
        # Agent as primary manager
        agent_rel = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'context': 'Day-to-day management'
            }
        )
        
        # User as sponsor
        user_rel = self.user.manages_projects.connect(
            self.project,
            {
                'role': 'sponsor',
                'is_primary': False,
                'context': 'Executive oversight'
            }
        )
        
        # Verify from project perspective
        managers = self.project.managed_by  # This is already a list
        assert len(managers) == 2
        
        # Verify manager types
        manager_names = []
        for manager in managers:
            if hasattr(manager, 'name'):
                manager_names.append(manager.name)
            elif hasattr(manager, 'username'):
                manager_names.append(manager.username)
        
        assert self.agent.name in manager_names
        assert self.user.username in manager_names
    
    def test_management_relationship_update(self):
        """Test update ManagesProjectRel properties"""
        # Create initial relationship
        relationship = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'coordinator',
                'is_primary': False,
                'context': 'Initial coordination role'
            }
        )
        
        initial_assigned_date = relationship.assigned_at
        
        # Update relationship properties
        relationship.role = 'project_manager'
        relationship.is_primary = True
        relationship.context = 'Promoted to primary manager'
        relationship.notes = 'Promotion due to excellent performance'
        relationship.save()
        
        # Verify updates
        updated_rel = self.agent.manages_projects.relationship(self.project)
        assert updated_rel.role == 'project_manager'
        assert updated_rel.is_primary == True
        assert updated_rel.context == 'Promoted to primary manager'
        assert updated_rel.notes == 'Promotion due to excellent performance'
        assert updated_rel.assigned_at == initial_assigned_date  # Should not change
    
    def test_management_relationship_deletion(self):
        """Test xóa ManagesProjectRel relationship"""
        # Create relationship
        self.agent.manages_projects.connect(
            self.project,
            {'role': 'project_manager', 'is_primary': True}
        )
        
        # Verify relationship exists
        assert len(self.agent.manages_projects.all()) == 1
        assert len(self.project.managed_by) == 1
        
        # Delete relationship
        self.agent.manages_projects.disconnect(self.project)
        
        # Verify deletion
        assert len(self.agent.manages_projects.all()) == 0
        assert len(self.project.managed_by) == 0


class TestManagesProjectRelValidation:
    """Test business rules và validation cho ManagesProjectRel"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_client = TestClient(app)
        
        self.agent = Agent(
            name="Test Manager Agent",
            description="Test management agent",
            agent_type="AIAgent",
            status="active"
        ).save()
        
        self.project = Project(
            title=f"Test Project {uuid.uuid4().hex[:8]}",
            description="Test project",
            status="planning"
        ).save()
    
    def teardown_method(self):
        """Cleanup"""
        if hasattr(self, 'agent') and self.agent:
            for rel in self.agent.manages_projects.all():
                rel.delete()
            self.agent.delete()
            
        if hasattr(self, 'project') and self.project:
            self.project.delete()
    
    def test_management_role_types(self):
        """Test different management role types"""
        management_roles = [
            'project_manager',
            'sponsor',
            'coordinator',
            'scrum_master',
            'product_owner',
            'stakeholder'
        ]
        
        for role in management_roles:
            # Delete previous relationship if exists
            try:
                self.agent.manages_projects.disconnect(self.project)
            except:
                pass
            
            # Create relationship with specific role
            relationship = self.agent.manages_projects.connect(
                self.project,
                {
                    'role': role,
                    'is_primary': role == 'project_manager',  # PM is usually primary
                    'context': f'Testing {role} role'
                }
            )
            
            assert relationship.role == role
            print(f"✅ Management role '{role}' validated")
    
    def test_primary_manager_logic(self):
        """Test primary manager designation"""
        # Test primary manager
        primary_rel = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'context': 'Primary management responsibility'
            }
        )
        
        assert primary_rel.is_primary == True
        
        # Test secondary manager
        self.agent.manages_projects.disconnect(self.project)
        
        secondary_rel = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'sponsor',
                'is_primary': False,
                'context': 'Supporting role'
            }
        )
        
        assert secondary_rel.is_primary == False
    
    def test_default_values(self):
        """Test default values cho optional properties"""
        relationship = self.agent.manages_projects.connect(
            self.project,
            {'role': 'project_manager'}  # Only required field
        )
        
        # Test default values
        assert relationship.role == 'project_manager'
        assert relationship.is_primary == True  # Default primary
        assert relationship.assigned_at is not None
        # context and notes can be None
    
    def test_assignment_date_tracking(self):
        """Test assignment date tracking và automatic timestamps"""
        # Create relationship
        relationship = self.agent.manages_projects.connect(
            self.project,
            {'role': 'project_manager', 'is_primary': True}
        )
        
        # Verify assignment date is set
        assigned_at = relationship.assigned_at
        assert assigned_at is not None
        assert isinstance(assigned_at, datetime)
        
        # Verify the date is recent (within last minute)
        now = datetime.now()
        if assigned_at.tzinfo is not None:
            # Convert to naive datetime for comparison
            assigned_at = assigned_at.replace(tzinfo=None)
        
        time_diff = abs((now - assigned_at).total_seconds())
        assert time_diff < 60  # Should be within last minute
    
    def test_context_and_notes_flexibility(self):
        """Test context và notes properties"""
        long_context = "This is a comprehensive management context that explains the full scope of responsibilities, expectations, and deliverables for this management relationship."
        
        long_notes = "Detailed notes about performance expectations, reporting structure, decision-making authority, budget responsibility, and other important management considerations."
        
        relationship = self.agent.manages_projects.connect(
            self.project,
            {
                'role': 'project_manager',
                'context': long_context,
                'notes': long_notes,
                'is_primary': True
            }
        )
        
        assert relationship.context == long_context
        assert relationship.notes == long_notes


class TestManagesProjectRelComplexOperations:
    """Test complex operations và workflows cho ManagesProjectRel"""
    
    def setup_method(self):
        """Setup complex test scenario"""
        self.test_client = TestClient(app)
        
        # Create multiple managers
        self.agents = []
        for i in range(3):
            agent = Agent(
                name=f"Manager Agent {i+1}",
                description=f"Management agent {i+1}",
                agent_type="AIAgent",
                status="active"
            ).save()
            self.agents.append(agent)
        
        self.users = []
        for i in range(2):
            user = User(
                username=f"manager_{i+1}_{uuid.uuid4().hex[:8]}",
                email=f"manager{i+1}@example.com",
                full_name=f"Manager User {i+1}"
            ).save()
            self.users.append(user)
        
        # Create multiple projects
        self.projects = []
        project_types = ["Software Development", "Infrastructure", "Research", "Marketing"]
        for i, project_type in enumerate(project_types):
            project = Project(
                title=f"{project_type} Project {uuid.uuid4().hex[:8]}",
                description=f"{project_type} project for testing",
                status="planning" if i % 2 == 0 else "active"
            ).save()
            self.projects.append(project)
    
    def teardown_method(self):
        """Cleanup all test data"""
        # Clean up relationships first
        for agent in self.agents:
            for rel in agent.manages_projects.all():
                rel.delete()
            agent.delete()
        
        for user in self.users:
            for rel in user.manages_projects.all():
                rel.delete()
            user.delete()
        
        for project in self.projects:
            project.delete()
    
    def test_project_management_hierarchy(self):
        """Test hierarchical project management structure"""
        target_project = self.projects[0]
        
        # Create management hierarchy
        # Primary PM (Agent)
        primary_pm = self.agents[0].manages_projects.connect(
            target_project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'context': 'Primary project manager',
                'notes': 'Full responsibility for project delivery'
            }
        )
        
        # Sponsor (User)
        sponsor = self.users[0].manages_projects.connect(
            target_project,
            {
                'role': 'sponsor',
                'is_primary': False,
                'context': 'Executive sponsor',
                'notes': 'Strategic oversight and funding approval'
            }
        )
        
        # Scrum Master (Agent)
        scrum_master = self.agents[1].manages_projects.connect(
            target_project,
            {
                'role': 'scrum_master',
                'is_primary': False,
                'context': 'Agile process facilitation',
                'notes': 'Daily standup and sprint management'
            }
        )
        
        # Verify hierarchy
        all_managers = target_project.managed_by  # Already a list
        assert len(all_managers) == 3
        
        # Verify role distribution
        management_roles = []
        for manager in all_managers:
            if hasattr(manager, 'manages_projects'):  # Agent
                rel = manager.manages_projects.relationship(target_project)
            else:  # User
                rel = manager.manages_projects.relationship(target_project)
            management_roles.append(rel.role)
        
        assert 'project_manager' in management_roles
        assert 'sponsor' in management_roles
        assert 'scrum_master' in management_roles
        
        # Find primary manager
        primary_managers = []
        for manager in all_managers:
            if hasattr(manager, 'manages_projects'):  # Agent
                rel = manager.manages_projects.relationship(target_project)
            else:  # User
                rel = manager.manages_projects.relationship(target_project)
            if rel.is_primary:
                primary_managers.append(manager)
        
        assert len(primary_managers) == 1  # Only one primary manager
    
    def test_cross_project_management_portfolio(self):
        """Test manager handling multiple projects (portfolio management)"""
        portfolio_manager = self.agents[0]
        
        # Assign different roles across multiple projects
        project_assignments = [
            (self.projects[0], 'project_manager', True, 'Lead development project'),
            (self.projects[1], 'coordinator', False, 'Supporting infrastructure setup'),
            (self.projects[2], 'stakeholder', False, 'Research project oversight'),
            (self.projects[3], 'project_manager', True, 'Marketing campaign lead')
        ]
        
        for project, role, is_primary, context in project_assignments:
            relationship = portfolio_manager.manages_projects.connect(
                project,
                {
                    'role': role,
                    'is_primary': is_primary,
                    'context': context,
                    'notes': f'Portfolio assignment for {project.title}'
                }
            )
        
        # Verify portfolio
        managed_projects = portfolio_manager.manages_projects.all()
        assert len(managed_projects) == 4
        
        # Verify role diversity
        roles_assigned = []
        primary_count = 0
        
        for project in managed_projects:
            rel = portfolio_manager.manages_projects.relationship(project)
            roles_assigned.append(rel.role)
            if rel.is_primary:
                primary_count += 1
        
        assert len(set(roles_assigned)) > 1  # Multiple different roles
        assert primary_count == 2  # Two primary management roles
        
        # Verify specific role assignments
        assert 'project_manager' in roles_assigned
        assert 'coordinator' in roles_assigned
        assert 'stakeholder' in roles_assigned
    
    def test_management_role_transitions(self):
        """Test role transitions và promotions"""
        agent = self.agents[0]
        project = self.projects[0]
        
        # Start as coordinator
        initial_rel = agent.manages_projects.connect(
            project,
            {
                'role': 'coordinator',
                'is_primary': False,
                'context': 'Starting as project coordinator',
                'notes': 'New team member learning the project'
            }
        )
        
        assert initial_rel.role == 'coordinator'
        assert initial_rel.is_primary == False
        
        # Promote to project manager
        initial_rel.role = 'project_manager'
        initial_rel.is_primary = True
        initial_rel.context = 'Promoted to project manager'
        initial_rel.notes = 'Demonstrated excellent coordination skills'
        initial_rel.save()
        
        # Verify promotion
        updated_rel = agent.manages_projects.relationship(project)
        assert updated_rel.role == 'project_manager'
        assert updated_rel.is_primary == True
        assert updated_rel.context == 'Promoted to project manager'
        
        # Further transition to senior role
        updated_rel.role = 'senior_project_manager'
        updated_rel.context = 'Promoted to senior project manager'
        updated_rel.notes = 'Leading multiple projects successfully'
        updated_rel.save()
        
        # Verify final state
        final_rel = agent.manages_projects.relationship(project)
        assert final_rel.role == 'senior_project_manager'
        assert final_rel.is_primary == True
    
    def test_temporary_management_assignments(self):
        """Test temporary và interim management assignments"""
        regular_manager = self.agents[0]
        interim_manager = self.agents[1]
        project = self.projects[0]
        
        # Regular manager assignment
        regular_rel = regular_manager.manages_projects.connect(
            project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'context': 'Regular project manager',
                'notes': 'Permanent assignment'
            }
        )
        
        # Simulate temporary unavailability - remove regular manager
        regular_manager.manages_projects.disconnect(project)
        
        # Assign interim manager
        interim_rel = interim_manager.manages_projects.connect(
            project,
            {
                'role': 'interim_project_manager',
                'is_primary': True,
                'context': 'Temporary management during regular PM absence',
                'notes': 'Covering for regular PM during vacation/leave'
            }
        )
        
        # Verify interim management
        project_managers = project.managed_by  # Already a list
        assert len(project_managers) == 1
        assert project_managers[0].name == interim_manager.name
        
        interim_rel_check = interim_manager.manages_projects.relationship(project)
        assert interim_rel_check.role == 'interim_project_manager'
        assert interim_rel_check.is_primary == True
        
        # Return regular manager
        interim_manager.manages_projects.disconnect(project)
        
        restored_rel = regular_manager.manages_projects.connect(
            project,
            {
                'role': 'project_manager',
                'is_primary': True,
                'context': 'Returned from leave',
                'notes': 'Resumed regular management duties'
            }
        )
        
        # Verify restoration
        final_managers = project.managed_by  # Already a list
        assert len(final_managers) == 1
        assert final_managers[0].name == regular_manager.name


class TestManagesProjectRelPerformance:
    """Test performance và scalability cho ManagesProjectRel"""
    
    def setup_method(self):
        """Setup performance test scenario"""
        self.test_client = TestClient(app)
        
        # Create entities for bulk operations
        self.agents = []
        self.projects = []
        
        # Create 5 manager agents
        for i in range(5):
            agent = Agent(
                name=f"PM Agent {i+1}",
                description=f"Project management agent {i+1}",
                agent_type="AIAgent",
                status="active"
            ).save()
            self.agents.append(agent)
        
        # Create 10 projects
        project_categories = ["Software", "Infrastructure", "Research", "Marketing", "Operations"]
        for i in range(10):
            category = project_categories[i % len(project_categories)]
            project = Project(
                title=f"{category} Project {i+1} {uuid.uuid4().hex[:8]}",
                description=f"{category} project for performance testing",
                status="planning" if i % 2 == 0 else "active"
            ).save()
            self.projects.append(project)
    
    def teardown_method(self):
        """Cleanup performance test data"""
        # Clean up relationships first
        for agent in self.agents:
            for rel in agent.manages_projects.all():
                rel.delete()
            agent.delete()
        
        for project in self.projects:
            project.delete()
    
    def test_bulk_management_assignment(self):
        """Test bulk management assignment performance"""
        start_time = datetime.now()
        
        # Assign projects to managers (5 agents × 4 projects each = 20 relationships)
        relationship_count = 0
        management_roles = ['project_manager', 'coordinator', 'sponsor', 'stakeholder']
        
        for i, agent in enumerate(self.agents):
            # Each agent manages 4 projects with different roles
            for j in range(4):
                project = self.projects[i * 2 + j % 2]  # Overlap some assignments
                role = management_roles[j]
                is_primary = (role == 'project_manager')
                
                relationship = agent.manages_projects.connect(
                    project,
                    {
                        'role': role,
                        'is_primary': is_primary,
                        'context': f'{role} assignment for performance test',
                        'notes': f'Bulk assignment {relationship_count + 1}'
                    }
                )
                relationship_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Verify all relationships created
        assert relationship_count == 20  # 5 agents × 4 assignments
        
        # Verify performance (should complete within reasonable time)
        assert duration < 30.0  # 30 seconds maximum
        print(f"✅ Created {relationship_count} management relationships in {duration:.2f} seconds")
        
        # Verify data integrity
        total_managed_projects = 0
        for agent in self.agents:
            managed_projects = agent.manages_projects.all()
            total_managed_projects += len(managed_projects)
        
        assert total_managed_projects == 20
    
    def test_management_query_performance(self):
        """Test query performance với large management dataset"""
        # First create relationships
        for i, agent in enumerate(self.agents):
            for j, project in enumerate(self.projects[:6]):  # Each agent manages 6 projects
                role = 'project_manager' if j == 0 else 'coordinator'
                agent.manages_projects.connect(
                    project,
                    {
                        'role': role,
                        'is_primary': (j == 0),
                        'context': f'Performance test assignment {i}-{j}'
                    }
                )
        
        # Test query performance
        start_time = datetime.now()
        
        # Query all projects for each agent
        total_projects_found = 0
        for agent in self.agents:
            managed_projects = agent.manages_projects.all()
            total_projects_found += len(managed_projects)
        
        # Query all managers for each project
        total_managers_found = 0
        for project in self.projects[:6]:
            project_managers = project.managed_by  
            total_managers_found += len(project_managers)
        
        end_time = datetime.now()
        query_duration = (end_time - start_time).total_seconds()
        
        # Verify query results
        assert total_projects_found == 30  # 5 agents × 6 projects
        assert total_managers_found == 30  # 6 projects × 5 managers
        
        # Verify query performance
        assert query_duration < 10.0  # 10 seconds maximum
        print(f"✅ Queried {total_projects_found + total_managers_found} management relationships in {query_duration:.2f} seconds")
    
    def test_management_role_filtering(self):
        """Test filtering by management roles và responsibilities"""
        # Create diverse management assignments
        management_roles = ['project_manager', 'sponsor', 'coordinator', 'scrum_master', 'stakeholder']
        
        for i, agent in enumerate(self.agents):
            for j, project in enumerate(self.projects[:3]):  # 3 projects per agent
                role = management_roles[j % len(management_roles)]
                is_primary = (role == 'project_manager')
                
                agent.manages_projects.connect(
                    project,
                    {
                        'role': role,
                        'is_primary': is_primary,
                        'context': f'{role} for performance testing',
                        'notes': f'Agent {i+1} as {role}'
                    }
                )
        
        # Test filtering primary managers
        primary_manager_assignments = []
        for agent in self.agents:
            managed_projects = agent.manages_projects.all()
            for project in managed_projects:
                rel = agent.manages_projects.relationship(project)
                if rel.is_primary:
                    primary_manager_assignments.append((agent, project, rel))
        
        assert len(primary_manager_assignments) > 0
        print(f"✅ Found {len(primary_manager_assignments)} primary management assignments")
        
        # Test filtering by role type
        project_manager_assignments = []
        sponsor_assignments = []
        
        for agent in self.agents:
            managed_projects = agent.manages_projects.all()
            for project in managed_projects:
                rel = agent.manages_projects.relationship(project)
                if rel.role == 'project_manager':
                    project_manager_assignments.append((agent, project))
                elif rel.role == 'sponsor':
                    sponsor_assignments.append((agent, project))
        
        assert len(project_manager_assignments) > 0
        print(f"✅ Found {len(project_manager_assignments)} project manager assignments")
        print(f"✅ Found {len(sponsor_assignments)} sponsor assignments") 