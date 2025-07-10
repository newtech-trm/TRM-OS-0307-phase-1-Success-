"""
Comprehensive integration tests for AssignedToProjectRel relationship.

This file tests the ASSIGNED_TO_PROJECT relationship between Resource and Project entities,
following the TRM-OS ontology specifications and COMPREHENSIVE_COVERAGE_ANALYSIS.md requirements.

Tests cover:
- CRUD operations for AssignedToProjectRel
- Different allocation types and percentages
- Assignment status transitions
- Resource assignment validation
- Multiple resource assignment scenarios
- Bulk assignment operations
- Assignment period management
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from trm_api.main import app

# Graph Models - Direct imports for database operations
from trm_api.graph_models.resource import Resource as GraphResource
from trm_api.graph_models.project import Project as GraphProject
from trm_api.graph_models.assigned_to_project import AssignedToProjectRel

# Repositories for advanced operations
from trm_api.repositories.resource_repository import ResourceRepository

class TestAssignedToProjectRelCRUD:
    """Test basic CRUD operations for AssignedToProjectRel"""
    
    @pytest.fixture
    def test_client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def cleanup_resources(self):
        """Clean up resources after tests"""
        created_resources = []
        created_projects = []
        yield created_resources, created_projects
        
        # Cleanup
        for resource in created_resources:
            try:
                if hasattr(resource, 'delete'):
                    resource.delete()
                elif hasattr(resource, 'uid'):
                    # Try to find and delete
                    found = GraphResource.nodes.get_or_none(uid=resource.uid)
                    if found:
                        found.delete()
            except Exception:
                pass
                
        for project in created_projects:
            try:
                if hasattr(project, 'delete'):
                    project.delete()
                elif hasattr(project, 'uid'):
                    # Try to find and delete
                    found = GraphProject.nodes.get_or_none(uid=project.uid)
                    if found:
                        found.delete()
            except Exception:
                pass

    def test_create_basic_assignment(self, test_client, cleanup_resources):
        """Test creating basic Resource→Project assignment"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource using fixed method
        resource = GraphResource.create_single(
            name="Senior Developer",
            description="Experienced full-stack developer",
            resourceType="Human"
        )
        created_resources.append(resource)
        
        # Create Project with required title field
        project = GraphProject(
            title="E-Commerce Platform Development",
            description="Building next-gen e-commerce platform",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create assignment relationship
        assignment = resource.assigned_to_projects.connect(project, {
            'allocation_percentage': 75,
            'assignment_type': 'partial',
            'assignment_status': 'active',
            'notes': 'Lead developer for frontend components'
        })
        
        # Verify assignment
        assert assignment is not None
        assert assignment.allocation_percentage == 75
        assert assignment.assignment_type == 'partial'
        assert assignment.assignment_status == 'active'
        assert assignment.notes == 'Lead developer for frontend components'
        
        # Verify from project side
        assigned_resources = project.assigned_resources.all()
        assert len(assigned_resources) == 1
        assert assigned_resources[0].uid == resource.uid

    def test_create_full_allocation_assignment(self, test_client, cleanup_resources):
        """Test full allocation assignment (100%)"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource
        resource = GraphResource.create_single(
            name="Project Management Software",
            description="Enterprise project management tool license",
            resourceType="Tool"
        )
        created_resources.append(resource)
        
        # Create Project
        project = GraphProject(
            title="Team Productivity Initiative",
            description="Improving team collaboration and productivity",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create full allocation assignment
        expected_end = datetime.now() + timedelta(days=90)
        assignment = resource.assigned_to_projects.connect(project, {
            'allocation_percentage': 100,
            'assignment_type': 'full',
            'assignment_status': 'active',
            'expected_end_date': expected_end
        })
        
        # Verify assignment
        assert assignment.allocation_percentage == 100
        assert assignment.assignment_type == 'full'
        assert assignment.assignment_status == 'active'
        assert assignment.expected_end_date is not None

    def test_create_on_demand_assignment(self, test_client, cleanup_resources):
        """Test on-demand assignment type"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource
        resource = GraphResource.create_single(
            name="Cloud Infrastructure Budget",
            description="AWS cloud budget allocation",
            resourceType="Financial"
        )
        created_resources.append(resource)
        
        # Create Project
        project = GraphProject(
            title="Cloud Migration Project",
            description="Migrating legacy systems to cloud",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create on-demand assignment
        assignment = resource.assigned_to_projects.connect(project, {
            'allocation_percentage': 50,
            'assignment_type': 'on-demand',
            'assignment_status': 'active',
            'notes': 'Budget available on-demand for scaling needs'
        })
        
        # Verify assignment
        assert assignment.assignment_type == 'on-demand'
        assert assignment.allocation_percentage == 50

class TestAssignedToProjectRelValidation:
    """Test validation and business rules for AssignedToProjectRel"""
    
    @pytest.fixture
    def test_client(self):
        return TestClient(app)
    
    @pytest.fixture
    def cleanup_resources(self):
        created_resources = []
        created_projects = []
        yield created_resources, created_projects
        
        for resource in created_resources:
            try:
                if hasattr(resource, 'delete'):
                    resource.delete()
            except Exception:
                pass
                
        for project in created_projects:
            try:
                if hasattr(project, 'delete'):
                    project.delete()
            except Exception:
                pass

    def test_assignment_percentage_validation(self, test_client, cleanup_resources):
        """Test allocation percentage validation (0-100)"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource and Project
        resource = GraphResource.create_single(
            name="QA Engineer",
            resourceType="Human"
        )
        created_resources.append(resource)
        
        project = GraphProject(
            title="Quality Assurance Project",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Test valid percentages
        valid_percentages = [0, 25, 50, 75, 100]
        for percentage in valid_percentages:
            assignment = resource.assigned_to_projects.connect(project, {
                'allocation_percentage': percentage
            })
            assert assignment.allocation_percentage == percentage
            
            # Disconnect for next test
            resource.assigned_to_projects.disconnect(project)

    def test_assignment_status_transitions(self, test_client, cleanup_resources):
        """Test valid assignment status transitions"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource and Project
        resource = GraphResource.create_single(
            name="Conference Room A",
            resourceType="Space"
        )
        created_resources.append(resource)
        
        project = GraphProject(
            title="Team Collaboration Hub",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create assignment
        assignment = resource.assigned_to_projects.connect(project, {
            'assignment_status': 'active'
        })
        
        # Test status transitions
        valid_statuses = ['active', 'on-hold', 'completed', 'cancelled']
        
        for status in valid_statuses:
            # Update relationship properties
            rel = resource.assigned_to_projects.relationship(project)
            rel.assignment_status = status
            rel.save()
            
            # Verify update
            updated_rel = resource.assigned_to_projects.relationship(project)
            assert updated_rel.assignment_status == status

    def test_multiple_resources_same_project(self, test_client, cleanup_resources):
        """Test assigning multiple resources to same project"""
        created_resources, created_projects = cleanup_resources
        
        # Create multiple resources
        resources = []
        for i, resource_data in enumerate([
            ("Senior Developer", "Human"),
            ("Junior Developer", "Human"),
            ("Development Server", "Equipment"),
            ("Software Licenses", "Tool")
        ]):
            resource = GraphResource.create_single(
                name=resource_data[0],
                resourceType=resource_data[1]
            )
            resources.append(resource)
            created_resources.append(resource)
        
        # Create Project
        project = GraphProject(
            title="Multi-Resource Development Project",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Assign all resources to project
        allocations = [80, 60, 100, 100]  # Different allocation percentages
        for i, resource in enumerate(resources):
            assignment = resource.assigned_to_projects.connect(project, {
                'allocation_percentage': allocations[i],
                'assignment_type': 'partial' if allocations[i] < 100 else 'full',
                'assignment_status': 'active'
            })
            assert assignment.allocation_percentage == allocations[i]
        
        # Verify all assignments from project perspective
        assigned_resources = project.assigned_resources.all()
        assert len(assigned_resources) == 4
        
        # Verify each resource is properly assigned
        resource_uids = {r.uid for r in resources}
        assigned_uids = {r.uid for r in assigned_resources}
        assert resource_uids == assigned_uids

class TestAssignedToProjectRelComplexOperations:
    """Test complex operations and workflows for AssignedToProjectRel"""
    
    @pytest.fixture
    def test_client(self):
        return TestClient(app)
    
    @pytest.fixture
    def cleanup_resources(self):
        created_resources = []
        created_projects = []
        yield created_resources, created_projects
        
        for resource in created_resources:
            try:
                if hasattr(resource, 'delete'):
                    resource.delete()
            except Exception:
                pass
                
        for project in created_projects:
            try:
                if hasattr(project, 'delete'):
                    project.delete()
            except Exception:
                pass

    def test_assignment_period_management(self, test_client, cleanup_resources):
        """Test assignment with specific start and end dates"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource and Project
        resource = GraphResource.create_single(
            name="Specialized Consultant",
            resourceType="Human"
        )
        created_resources.append(resource)
        
        project = GraphProject(
            title="Consultation Project",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create assignment with time bounds
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        
        assignment = resource.assigned_to_projects.connect(project, {
            'allocation_percentage': 100,
            'assignment_type': 'full',
            'assignment_status': 'active',
            'assigned_at': start_date,
            'expected_end_date': end_date,
            'notes': '30-day consultation engagement'
        })
        
        # Verify assignment timing
        assert assignment.assigned_at.date() == start_date.date()
        assert assignment.expected_end_date.date() == end_date.date()
        assert assignment.notes == '30-day consultation engagement'
        
        # Test assignment completion
        actual_end = datetime.now() + timedelta(days=28)
        rel = resource.assigned_to_projects.relationship(project)
        rel.actual_end_date = actual_end
        rel.assignment_status = 'completed'
        rel.save()
        
        # Verify completion
        updated_rel = resource.assigned_to_projects.relationship(project)
        assert updated_rel.assignment_status == 'completed'
        assert updated_rel.actual_end_date.date() == actual_end.date()

    def test_resource_assignment_tracking(self, test_client, cleanup_resources):
        """Test tracking who assigned resources"""
        created_resources, created_projects = cleanup_resources
        
        # Create Resource and Project
        resource = GraphResource.create_single(
            name="Marketing Budget Q4",
            resourceType="Financial"
        )
        created_resources.append(resource)
        
        project = GraphProject(
            title="Q4 Marketing Campaign",
            status="active"
        ).save()
        created_projects.append(project)
        
        # Create assignment with assigned_by tracking
        assignment = resource.assigned_to_projects.connect(project, {
            'allocation_percentage': 100,
            'assignment_type': 'full',
            'assignment_status': 'active',
            'assigned_by': 'agent-pm-001',
            'notes': 'Approved by Project Manager for Q4 campaign'
        })
        
        # Verify assignment tracking
        assert assignment.assigned_by == 'agent-pm-001'
        assert assignment.notes == 'Approved by Project Manager for Q4 campaign'

    def test_bulk_resource_assignment(self, test_client, cleanup_resources):
        """Test bulk assignment of resources to multiple projects"""
        created_resources, created_projects = cleanup_resources
        
        # Create shared resource
        shared_resource = GraphResource.create_single(
            name="Cloud Infrastructure",
            resourceType="Equipment"
        )
        created_resources.append(shared_resource)
        
        # Create multiple projects
        projects = []
        for i in range(3):
            project = GraphProject(
                title=f"Project Alpha-{i+1}",
                status="active"
            ).save()
            projects.append(project)
            created_projects.append(project)
        
        # Assign shared resource to all projects with different allocations
        allocations = [40, 35, 25]  # Total = 100%
        
        for i, project in enumerate(projects):
            assignment = shared_resource.assigned_to_projects.connect(project, {
                'allocation_percentage': allocations[i],
                'assignment_type': 'partial',
                'assignment_status': 'active',
                'notes': f'Shared infrastructure allocation for Project Alpha-{i+1}'
            })
            assert assignment.allocation_percentage == allocations[i]
        
        # Verify all assignments from resource perspective
        assigned_projects = shared_resource.assigned_to_projects.all()
        assert len(assigned_projects) == 3
        
        # Verify total allocation doesn't exceed 100%
        total_allocation = sum(
            shared_resource.assigned_to_projects.relationship(project).allocation_percentage
            for project in assigned_projects
        )
        assert total_allocation == 100

class TestAssignedToProjectRelPerformance:
    """Test performance aspects of AssignedToProjectRel operations"""
    
    @pytest.fixture
    def test_client(self):
        return TestClient(app)
    
    @pytest.fixture
    def cleanup_resources(self):
        created_resources = []
        created_projects = []
        yield created_resources, created_projects
        
        for resource in created_resources:
            try:
                if hasattr(resource, 'delete'):
                    resource.delete()
            except Exception:
                pass
                
        for project in created_projects:
            try:
                if hasattr(project, 'delete'):
                    project.delete()
            except Exception:
                pass

    def test_large_scale_assignment_query(self, test_client, cleanup_resources):
        """Test querying assignments at scale"""
        created_resources, created_projects = cleanup_resources
        
        # Create multiple resources and projects
        resources = []
        projects = []
        
        # Create 5 resources
        for i in range(5):
            resource = GraphResource.create_single(
                name=f"Resource-{i+1}",
                resourceType="Tool"
            )
            resources.append(resource)
            created_resources.append(resource)
        
        # Create 3 projects
        for i in range(3):
            project = GraphProject(
                title=f"Performance Test Project-{i+1}",
                status="active"
            ).save()
            projects.append(project)
            created_projects.append(project)
        
        # Create multiple assignments (each resource to each project)
        assignment_count = 0
        for resource in resources:
            for project in projects:
                assignment = resource.assigned_to_projects.connect(project, {
                    'allocation_percentage': 20,  # 20% each
                    'assignment_type': 'partial',
                    'assignment_status': 'active'
                })
                assignment_count += 1
        
        # Verify total assignments created
        assert assignment_count == 15  # 5 resources × 3 projects
        
        # Test querying from different perspectives
        for project in projects:
            assigned_resources = project.assigned_resources.all()
            assert len(assigned_resources) == 5  # Each project has 5 resources
        
        for resource in resources:
            assigned_projects = resource.assigned_to_projects.all()
            assert len(assigned_projects) == 3  # Each resource assigned to 3 projects

    def test_assignment_filtering_and_searching(self, test_client, cleanup_resources):
        """Test filtering assignments by various criteria"""
        created_resources, created_projects = cleanup_resources
        
        # Create test data with different statuses
        resource = GraphResource.create_single(
            name="Multi-Status Resource",
            resourceType="Human"
        )
        created_resources.append(resource)
        
        projects_data = [
            ("Active Project", "active"),
            ("On-Hold Project", "on-hold"),
            ("Completed Project", "completed")
        ]
        
        projects = []
        for title, status in projects_data:
            project = GraphProject(title=title, status="active").save()
            projects.append(project)
            created_projects.append(project)
            
            # Create assignment with matching status
            assignment = resource.assigned_to_projects.connect(project, {
                'assignment_status': status,
                'allocation_percentage': 50
            })
        
        # Verify assignments with different statuses
        all_assigned_projects = resource.assigned_to_projects.all()
        assert len(all_assigned_projects) == 3
        
        # Check each assignment status
        for i, project in enumerate(projects):
            rel = resource.assigned_to_projects.relationship(project)
            expected_status = projects_data[i][1]
            assert rel.assignment_status == expected_status

if __name__ == "__main__":
    pytest.main([__file__]) 