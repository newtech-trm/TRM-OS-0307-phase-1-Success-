"""
Comprehensive Integration Tests for RequiresResourceRel relationship.
Tests Project/Task -> Resource requirement relationships với đầy đủ validation, performance và edge cases.
"""

import pytest
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from trm_api.main import app
from trm_api.graph_models.project import Project
from trm_api.graph_models.task import Task
from trm_api.graph_models.resource import Resource
from trm_api.graph_models.requires_resource import RequiresResourceRel


class TestRequiresResourceRelCRUD:
    """Test basic CRUD operations cho RequiresResourceRel"""
    
    def setup_method(self):
        """Setup test data cho mỗi test"""
        self.test_client = TestClient(app)
        
        # Tạo test entities
        self.project = Project(
            title=f"Resource Requirement Project {uuid.uuid4().hex[:8]}",
            description="Project for testing resource requirements",
            status="planning"
        ).save()
        
        self.task = Task(
            name=f"Resource Task {uuid.uuid4().hex[:8]}",
            description="Task requiring resources",
            status="ToDo"
        ).save()
        
        self.hardware_resource = Resource.create_single(
            name=f"Server Hardware {uuid.uuid4().hex[:8]}",
            description="High-performance server for computation",
            resourceType="hardware",
            status="available"
        )
        
        self.software_resource = Resource.create_single(
            name=f"Software License {uuid.uuid4().hex[:8]}",
            description="Premium software license",
            resourceType="software",
            status="limited"
        )
        
        self.human_resource = Resource.create_single(
            name=f"Developer Expertise {uuid.uuid4().hex[:8]}",
            description="Senior developer skills",
            resourceType="human",
            status="allocated"
        )
    
    def teardown_method(self):
        """Cleanup sau mỗi test"""
        # Delete relationships first
        if hasattr(self, 'project') and self.project:
            for rel in self.project.requires_resources.all():
                rel.delete()
            self.project.delete()
            
        if hasattr(self, 'task') and self.task:
            for rel in self.task.requires_resources.all():
                rel.delete()
            self.task.delete()
            
        if hasattr(self, 'hardware_resource') and self.hardware_resource:
            self.hardware_resource.delete()
        if hasattr(self, 'software_resource') and self.software_resource:
            self.software_resource.delete()
        if hasattr(self, 'human_resource') and self.human_resource:
            self.human_resource.delete()
    
    def test_project_requires_resource_creation(self):
        """Test Project -> Resource requirement relationship creation"""
        # Create resource requirement
        relationship = self.project.requires_resources.connect(
            self.hardware_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 3,
                'priorityLevel': 1,  # Critical
                'isAvailable': False,
                'estimatedCost': 50000.0,
                'procurementDeadline': datetime.now() + timedelta(days=30),
                'notes': 'High-performance servers for data processing'
            }
        )
        
        # Verify relationship exists
        assert relationship is not None
        assert relationship.quantityNeeded == 3
        assert relationship.priorityLevel == 1
        assert relationship.isAvailable == False
        assert relationship.estimatedCost == 50000.0
        assert relationship.notes == 'High-performance servers for data processing'
        assert relationship.creationDate is not None
        assert relationship.procurementDeadline is not None
        
        # Verify from project side
        required_resources = self.project.requires_resources.all()
        assert len(required_resources) == 1
        assert required_resources[0].name == self.hardware_resource.name
    
    def test_task_requires_resource_creation(self):
        """Test Task -> Resource requirement relationship creation"""
        # Create resource requirement
        relationship = self.task.requires_resources.connect(
            self.software_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 2,  # High
                'isAvailable': True,
                'estimatedCost': 2500.0,
                'actualCost': 2400.0,
                'allocatedBy': 'project_manager_001',
                'allocatedDate': datetime.now(),
                'notes': 'Software license for development tools'
            }
        )
        
        # Verify relationship
        assert relationship.quantityNeeded == 1
        assert relationship.priorityLevel == 2
        assert relationship.isAvailable == True
        assert relationship.estimatedCost == 2500.0
        assert relationship.actualCost == 2400.0
        assert relationship.allocatedBy == 'project_manager_001'
        assert relationship.allocatedDate is not None
    
    def test_multiple_resources_per_project(self):
        """Test Project requiring multiple resources"""
        # Connect multiple resources with different requirements
        hw_rel = self.project.requires_resources.connect(
            self.hardware_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 40000.0
            }
        )
        
        sw_rel = self.project.requires_resources.connect(
            self.software_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 5,
                'priorityLevel': 2,  # High
                'estimatedCost': 12500.0
            }
        )
        
        hr_rel = self.project.requires_resources.connect(
            self.human_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 80000.0
            }
        )
        
        # Verify all relationships
        required_resources = self.project.requires_resources.all()
        assert len(required_resources) == 3
        
        resource_names = [resource.name for resource in required_resources]
        assert self.hardware_resource.name in resource_names
        assert self.software_resource.name in resource_names
        assert self.human_resource.name in resource_names
        
        # Verify different priority levels
        total_critical = 0
        total_high = 0
        for resource in required_resources:
            rel = self.project.requires_resources.relationship(resource)
            if rel.priorityLevel == 1:
                total_critical += 1
            elif rel.priorityLevel == 2:
                total_high += 1
        
        assert total_critical == 2  # Hardware and Human
        assert total_high == 1  # Software
    
    def test_resource_requirement_update(self):
        """Test update RequiresResourceRel properties"""
        # Create initial requirement
        relationship = self.project.requires_resources.connect(
            self.hardware_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 3,  # Medium
                'isAvailable': False,
                'estimatedCost': 25000.0
            }
        )
        
        initial_creation_date = relationship.creationDate
        
        # Update requirement properties
        relationship.quantityNeeded = 2
        relationship.priorityLevel = 1  # Upgrade to Critical
        relationship.isAvailable = True
        relationship.actualCost = 48000.0
        relationship.allocatedBy = 'resource_manager_001'
        relationship.allocatedDate = datetime.now()
        relationship.lastModifiedDate = datetime.now()
        relationship.save()
        
        # Verify updates
        updated_rel = self.project.requires_resources.relationship(self.hardware_resource)
        assert updated_rel.quantityNeeded == 2
        assert updated_rel.priorityLevel == 1
        assert updated_rel.isAvailable == True
        assert updated_rel.actualCost == 48000.0
        assert updated_rel.allocatedBy == 'resource_manager_001'
        assert updated_rel.creationDate == initial_creation_date  # Should not change
        assert updated_rel.lastModifiedDate > initial_creation_date
    
    def test_resource_requirement_deletion(self):
        """Test xóa RequiresResourceRel relationship"""
        # Create requirement
        self.project.requires_resources.connect(
            self.hardware_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 3
            }
        )
        
        # Verify requirement exists
        assert len(self.project.requires_resources.all()) == 1
        
        # Delete requirement
        self.project.requires_resources.disconnect(self.hardware_resource)
        
        # Verify deletion
        assert len(self.project.requires_resources.all()) == 0


class TestRequiresResourceRelValidation:
    """Test business rules và validation cho RequiresResourceRel"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_client = TestClient(app)
        
        self.project = Project(
            title=f"Validation Project {uuid.uuid4().hex[:8]}",
            description="Project for validation testing",
            status="planning"
        ).save()
        
        self.resource = Resource.create_single(
            name=f"Test Resource {uuid.uuid4().hex[:8]}",
            description="Resource for validation",
            resourceType="hardware",
            status="available"
        )
    
    def teardown_method(self):
        """Cleanup"""
        if hasattr(self, 'project') and self.project:
            for rel in self.project.requires_resources.all():
                rel.delete()
            self.project.delete()
            
        if hasattr(self, 'resource') and self.resource:
            self.resource.delete()
    
    def test_priority_levels_validation(self):
        """Test tất cả priority levels (1-5)"""
        priority_levels = {
            1: "Critical",
            2: "High", 
            3: "Medium",
            4: "Low",
            5: "Optional"
        }
        
        for level, description in priority_levels.items():
            # Delete previous relationship if exists
            try:
                self.project.requires_resources.disconnect(self.resource)
            except:
                pass
            
            # Create requirement with specific priority level
            relationship = self.project.requires_resources.connect(
                self.resource,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'quantityNeeded': 1,
                    'priorityLevel': level
                }
            )
            
            assert relationship.priorityLevel == level
            print(f"✅ Priority Level {level} ({description}) validated")
    
    def test_quantity_validation(self):
        """Test quantity needed validation"""
        test_quantities = [1, 5, 10, 50, 100]
        
        for quantity in test_quantities:
            try:
                self.project.requires_resources.disconnect(self.resource)
            except:
                pass
            
            relationship = self.project.requires_resources.connect(
                self.resource,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'quantityNeeded': quantity,
                    'priorityLevel': 3
                }
            )
            
            assert relationship.quantityNeeded == quantity
    
    def test_cost_tracking_validation(self):
        """Test cost tracking fields"""
        relationship = self.project.requires_resources.connect(
            self.resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'estimatedCost': 10000.0,
                'actualCost': 9500.0
            }
        )
        
        # Verify cost tracking
        assert relationship.estimatedCost == 10000.0
        assert relationship.actualCost == 9500.0
        
        # Test cost variance calculation (would be done in business logic)
        cost_variance = relationship.actualCost - relationship.estimatedCost
        assert cost_variance == -500.0  # Under budget
    
    def test_availability_tracking(self):
        """Test resource availability tracking"""
        # Test unavailable resource
        unavailable_rel = self.project.requires_resources.connect(
            self.resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'isAvailable': False,
                'priorityLevel': 1
            }
        )
        
        assert unavailable_rel.isAvailable == False
        
        # Update to available
        unavailable_rel.isAvailable = True
        unavailable_rel.allocatedBy = 'resource_manager'
        unavailable_rel.allocatedDate = datetime.now()
        unavailable_rel.save()
        
        updated_rel = self.project.requires_resources.relationship(self.resource)
        assert updated_rel.isAvailable == True
        assert updated_rel.allocatedBy == 'resource_manager'
        assert updated_rel.allocatedDate is not None
    
    def test_default_values(self):
        """Test default values cho properties"""
        relationship = self.project.requires_resources.connect(
            self.resource,
            {'relationshipId': str(uuid.uuid4())}  # Only required field
        )
        
        # Test default values
        assert relationship.quantityNeeded == 1  # Default quantity
        assert relationship.priorityLevel == 3  # Default medium priority
        assert relationship.isAvailable == False  # Default not available
        assert relationship.creationDate is not None
        assert relationship.lastModifiedDate is not None
    
    def test_deadline_tracking(self):
        """Test procurement deadline tracking"""
        from datetime import timezone
        future_deadline = datetime.now(timezone.utc) + timedelta(days=60)
        
        relationship = self.project.requires_resources.connect(
            self.resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'procurementDeadline': future_deadline,
                'notes': 'Must be procured before project phase 2'
            }
        )
        
        # Handle timezone-aware comparison
        deadline = relationship.procurementDeadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        assert deadline == future_deadline
        assert relationship.notes == 'Must be procured before project phase 2'
        
        # Test deadline proximity (business logic)
        now = datetime.now(timezone.utc)
        days_until_deadline = (deadline - now).days
        assert days_until_deadline > 0  # Future deadline


class TestRequiresResourceRelComplexOperations:
    """Test complex operations và workflows cho RequiresResourceRel"""
    
    def setup_method(self):
        """Setup complex test scenario"""
        self.test_client = TestClient(app)
        
        # Create multiple projects
        self.projects = []
        for i in range(3):
            project = Project(
                title=f"Complex Project {i+1}",
                description=f"Complex project {i+1} for testing",
                status="planning" if i % 2 == 0 else "active"
            ).save()
            self.projects.append(project)
        
        # Create multiple tasks
        self.tasks = []
        for i in range(2):
            task = Task(
                name=f"Complex Task {i+1}",
                description=f"Complex task {i+1}",
                status="ToDo"
            ).save()
            self.tasks.append(task)
        
        # Create resource categories
        self.hardware_resources = []
        self.software_resources = []
        self.human_resources = []
        
        # Hardware resources
        hw_types = ["Server", "Storage", "Network Equipment"]
        for hw_type in hw_types:
            resource = Resource.create_single(
                name=f"{hw_type} {uuid.uuid4().hex[:8]}",
                description=f"{hw_type} for complex operations",
                resourceType="hardware",
                status="available"
            )
            self.hardware_resources.append(resource)
        
        # Software resources
        sw_types = ["Database License", "Development Tools", "Monitoring Software"]
        for sw_type in sw_types:
            resource = Resource.create_single(
                name=f"{sw_type} {uuid.uuid4().hex[:8]}",
                description=f"{sw_type} for complex operations",
                resourceType="software",
                status="limited"
            )
            self.software_resources.append(resource)
        
        # Human resources
        hr_types = ["Backend Developer", "DevOps Engineer"]
        for hr_type in hr_types:
            resource = Resource.create_single(
                name=f"{hr_type} {uuid.uuid4().hex[:8]}",
                description=f"{hr_type} skills",
                resourceType="human",
                status="allocated"
            )
            self.human_resources.append(resource)
    
    def teardown_method(self):
        """Cleanup all test data"""
        # Clean up relationships first
        for project in self.projects:
            for rel in project.requires_resources.all():
                rel.delete()
            project.delete()
        
        for task in self.tasks:
            for rel in task.requires_resources.all():
                rel.delete()
            task.delete()
        
        for resource in self.hardware_resources + self.software_resources + self.human_resources:
            resource.delete()
    
    def test_project_resource_planning(self):
        """Test comprehensive project resource planning"""
        target_project = self.projects[0]
        
        # Hardware requirements
        server_req = target_project.requires_resources.connect(
            self.hardware_resources[0],  # Server
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 3,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 75000.0,
                'procurementDeadline': datetime.now() + timedelta(days=45),
                'notes': 'Production servers for application deployment'
            }
        )
        
        storage_req = target_project.requires_resources.connect(
            self.hardware_resources[1],  # Storage
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 30000.0,
                'procurementDeadline': datetime.now() + timedelta(days=30),
                'notes': 'High-capacity storage systems'
            }
        )
        
        # Software requirements
        db_req = target_project.requires_resources.connect(
            self.software_resources[0],  # Database License
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 2,  # High
                'estimatedCost': 15000.0,
                'procurementDeadline': datetime.now() + timedelta(days=20),
                'notes': 'Enterprise database license'
            }
        )
        
        # Human resources
        dev_req = target_project.requires_resources.connect(
            self.human_resources[0],  # Backend Developer
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 120000.0,
                'notes': 'Senior backend developers for 6 months'
            }
        )
        
        # Verify comprehensive resource plan
        required_resources = target_project.requires_resources.all()
        assert len(required_resources) == 4
        
        # Calculate total estimated cost
        total_cost = 0
        critical_resources = 0
        for resource in required_resources:
            rel = target_project.requires_resources.relationship(resource)
            total_cost += rel.estimatedCost or 0
            if rel.priorityLevel == 1:
                critical_resources += 1
        
        assert total_cost == 240000.0  # Sum of all costs
        assert critical_resources == 3  # Server, Storage, Developer
    
    def test_task_resource_dependencies(self):
        """Test task-level resource dependencies"""
        development_task = self.tasks[0]
        
        # Development task needs specific resources
        dev_tools_req = development_task.requires_resources.connect(
            self.software_resources[1],  # Development Tools
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 3,
                'priorityLevel': 2,  # High
                'estimatedCost': 9000.0,
                'isAvailable': True,
                'allocatedBy': 'tech_lead_001',
                'notes': 'IDE licenses for development team'
            }
        )
        
        developer_req = development_task.requires_resources.connect(
            self.human_resources[0],  # Backend Developer
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 1,  # Critical
                'estimatedCost': 20000.0,
                'isAvailable': False,
                'notes': 'Need to allocate developer to this task'
            }
        )
        
        # Verify task requirements
        task_resources = development_task.requires_resources.all()
        assert len(task_resources) == 2
        
        # Check availability status
        available_resources = 0
        for resource in task_resources:
            rel = development_task.requires_resources.relationship(resource)
            if rel.isAvailable:
                available_resources += 1
        
        assert available_resources == 1  # Only dev tools available
    
    def test_resource_allocation_workflow(self):
        """Test end-to-end resource allocation workflow"""
        project = self.projects[1]
        target_resource = self.hardware_resources[0]
        
        # Step 1: Initial requirement (not available)
        requirement = project.requires_resources.connect(
            target_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'priorityLevel': 1,
                'isAvailable': False,
                'estimatedCost': 50000.0,
                'procurementDeadline': datetime.now() + timedelta(days=30)
            }
        )
        
        assert requirement.isAvailable == False
        assert requirement.allocatedBy is None
        
        # Step 2: Resource becomes available
        requirement.isAvailable = True
        requirement.actualCost = 48000.0  # Slightly under budget
        requirement.allocatedBy = 'procurement_manager_001'
        requirement.allocatedDate = datetime.now()
        requirement.lastModifiedDate = datetime.now()
        requirement.save()
        
        # Step 3: Verify allocation
        updated_req = project.requires_resources.relationship(target_resource)
        assert updated_req.isAvailable == True
        assert updated_req.actualCost == 48000.0
        assert updated_req.allocatedBy == 'procurement_manager_001'
        assert updated_req.allocatedDate is not None
        
        # Step 4: Calculate cost savings
        cost_savings = updated_req.estimatedCost - updated_req.actualCost
        assert cost_savings == 2000.0  # $2000 under budget
    
    def test_cross_project_resource_contention(self):
        """Test resource contention across multiple projects"""
        shared_resource = self.hardware_resources[0]
        
        # Multiple projects requiring same resource
        project1_req = self.projects[0].requires_resources.connect(
            shared_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 2,
                'priorityLevel': 1,  # Critical
                'procurementDeadline': datetime.now() + timedelta(days=20),
                'notes': 'Project 1 urgent requirement'
            }
        )
        
        project2_req = self.projects[1].requires_resources.connect(
            shared_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 1,
                'priorityLevel': 2,  # High
                'procurementDeadline': datetime.now() + timedelta(days=30),
                'notes': 'Project 2 can wait if needed'
            }
        )
        
        project3_req = self.projects[2].requires_resources.connect(
            shared_resource,
            {
                'relationshipId': str(uuid.uuid4()),
                'quantityNeeded': 3,
                'priorityLevel': 1,  # Critical
                'procurementDeadline': datetime.now() + timedelta(days=15),
                'notes': 'Project 3 most urgent deadline'
            }
        )
        
        # Analyze resource contention
        total_quantity_needed = (
            project1_req.quantityNeeded + 
            project2_req.quantityNeeded + 
            project3_req.quantityNeeded
        )
        
        assert total_quantity_needed == 6  # Total demand
        
        # Priority analysis for resource allocation decisions
        critical_projects = []
        if project1_req.priorityLevel == 1:
            critical_projects.append(('Project 1', project1_req.quantityNeeded))
        if project2_req.priorityLevel == 1:
            critical_projects.append(('Project 2', project2_req.quantityNeeded))
        if project3_req.priorityLevel == 1:
            critical_projects.append(('Project 3', project3_req.quantityNeeded))
        
        assert len(critical_projects) == 2  # Projects 1 and 3 are critical
        
        # Deadline analysis
        earliest_deadline = min(
            project1_req.procurementDeadline,
            project2_req.procurementDeadline,
            project3_req.procurementDeadline
        )
        
        # Project 3 has earliest deadline
        assert earliest_deadline == project3_req.procurementDeadline


class TestRequiresResourceRelPerformance:
    """Test performance và scalability cho RequiresResourceRel"""
    
    def setup_method(self):
        """Setup performance test scenario"""
        self.test_client = TestClient(app)
        
        # Create entities for bulk operations
        self.projects = []
        self.resources = []
        
        # Create 3 projects
        for i in range(3):
            project = Project(
                title=f"Performance Project {i+1}",
                description=f"Performance test project {i+1}",
                status="planning"
            ).save()
            self.projects.append(project)
        
        # Create 8 resources of different types
        resource_types = ["hardware", "software", "human", "financial"]
        for i in range(8):
            resource_type = resource_types[i % len(resource_types)]
            resource = Resource.create_single(
                name=f"{resource_type.title()} Resource {i+1}",
                description=f"Performance test {resource_type} resource",
                resourceType=resource_type,
                status="available"
            )
            self.resources.append(resource)
    
    def teardown_method(self):
        """Cleanup performance test data"""
        # Clean up relationships first
        for project in self.projects:
            for rel in project.requires_resources.all():
                rel.delete()
            project.delete()
        
        for resource in self.resources:
            resource.delete()
    
    def test_bulk_resource_requirement_creation(self):
        """Test bulk resource requirement creation performance"""
        start_time = datetime.now()
        
        # Create requirements (3 projects × 8 resources = 24 relationships)
        relationship_count = 0
        priority_levels = [1, 2, 3, 4, 5]
        
        for i, project in enumerate(self.projects):
            for j, resource in enumerate(self.resources):
                priority = priority_levels[j % len(priority_levels)]
                quantity = (j % 3) + 1  # 1, 2, or 3
                cost = (j + 1) * 5000.0  # Varied costs
                
                relationship = project.requires_resources.connect(
                    resource,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'quantityNeeded': quantity,
                        'priorityLevel': priority,
                        'estimatedCost': cost,
                        'isAvailable': (j % 2 == 0),  # Alternate availability
                        'notes': f'Bulk requirement {relationship_count + 1}'
                    }
                )
                relationship_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Verify all relationships created
        assert relationship_count == 24  # 3 projects × 8 resources
        
        # Verify performance (should complete within reasonable time)
        assert duration < 30.0  # 30 seconds maximum
        print(f"✅ Created {relationship_count} resource requirements in {duration:.2f} seconds")
        
        # Verify data integrity
        total_requirements = 0
        for project in self.projects:
            project_requirements = project.requires_resources.all()
            total_requirements += len(project_requirements)
        
        assert total_requirements == 24
    
    def test_resource_requirement_query_performance(self):
        """Test query performance with large requirement dataset"""
        # First create requirements
        for i, project in enumerate(self.projects):
            for j, resource in enumerate(self.resources[:5]):  # 5 resources per project
                project.requires_resources.connect(
                    resource,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'quantityNeeded': j + 1,
                        'priorityLevel': (j % 3) + 1,
                        'estimatedCost': (j + 1) * 10000.0
                    }
                )
        
        # Test query performance
        start_time = datetime.now()
        
        # Query all requirements for each project
        total_requirements_found = 0
        for project in self.projects:
            required_resources = project.requires_resources.all()
            total_requirements_found += len(required_resources)
        
        end_time = datetime.now()
        query_duration = (end_time - start_time).total_seconds()
        
        # Verify query results
        assert total_requirements_found == 15  # 3 projects × 5 resources
        
        # Verify query performance
        assert query_duration < 10.0  # 10 seconds maximum
        print(f"✅ Queried {total_requirements_found} resource requirements in {query_duration:.2f} seconds")
    
    def test_resource_requirement_filtering(self):
        """Test filtering requirements by priority và availability"""
        # Create diverse requirements
        for i, project in enumerate(self.projects):
            for j, resource in enumerate(self.resources[:4]):  # 4 resources per project
                priority = ((i + j) % 5) + 1  # Varied priorities 1-5
                is_available = (j % 2 == 0)  # Alternate availability
                
                project.requires_resources.connect(
                    resource,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'quantityNeeded': j + 1,
                        'priorityLevel': priority,
                        'isAvailable': is_available,
                        'estimatedCost': (j + 1) * 15000.0
                    }
                )
        
        # Test filtering critical requirements (priority = 1)
        critical_requirements = []
        for project in self.projects:
            required_resources = project.requires_resources.all()
            for resource in required_resources:
                rel = project.requires_resources.relationship(resource)
                if rel.priorityLevel == 1:
                    critical_requirements.append((project, resource, rel))
        
        assert len(critical_requirements) > 0
        print(f"✅ Found {len(critical_requirements)} critical resource requirements")
        
        # Test filtering available requirements
        available_requirements = []
        for project in self.projects:
            required_resources = project.requires_resources.all()
            for resource in required_resources:
                rel = project.requires_resources.relationship(resource)
                if rel.isAvailable:
                    available_requirements.append((project, resource, rel))
        
        assert len(available_requirements) > 0
        print(f"✅ Found {len(available_requirements)} available resource requirements")
    
    def test_cost_aggregation_performance(self):
        """Test cost aggregation across multiple requirements"""
        # Create requirements with varied costs
        cost_multipliers = [1.0, 1.5, 2.0, 2.5, 3.0]
        
        for i, project in enumerate(self.projects):
            for j, resource in enumerate(self.resources[:3]):  # 3 resources per project
                base_cost = 20000.0
                multiplier = cost_multipliers[j % len(cost_multipliers)]
                estimated_cost = base_cost * multiplier
                actual_cost = estimated_cost * 0.9  # 10% under budget
                
                project.requires_resources.connect(
                    resource,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'quantityNeeded': 1,
                        'priorityLevel': 2,
                        'estimatedCost': estimated_cost,
                        'actualCost': actual_cost,
                        'isAvailable': True
                    }
                )
        
        # Test cost aggregation
        start_time = datetime.now()
        
        total_estimated_cost = 0
        total_actual_cost = 0
        
        for project in self.projects:
            required_resources = project.requires_resources.all()
            for resource in required_resources:
                rel = project.requires_resources.relationship(resource)
                total_estimated_cost += rel.estimatedCost or 0
                total_actual_cost += rel.actualCost or 0
        
        end_time = datetime.now()
        aggregation_duration = (end_time - start_time).total_seconds()
        
        # Verify cost calculations
        assert total_estimated_cost > 0
        assert total_actual_cost > 0
        assert total_actual_cost < total_estimated_cost  # Under budget
        
        cost_savings = total_estimated_cost - total_actual_cost
        savings_percentage = (cost_savings / total_estimated_cost) * 100
        
        assert savings_percentage > 5.0  # At least 5% savings
        
        # Verify performance
        assert aggregation_duration < 5.0  # 5 seconds maximum
        print(f"✅ Aggregated costs for {9} requirements in {aggregation_duration:.2f} seconds")
        print(f"✅ Total estimated: ${total_estimated_cost:,.2f}, Actual: ${total_actual_cost:,.2f}")
        print(f"✅ Cost savings: ${cost_savings:,.2f} ({savings_percentage:.1f}%)") 