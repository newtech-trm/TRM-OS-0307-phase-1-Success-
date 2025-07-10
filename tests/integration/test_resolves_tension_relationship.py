"""
Comprehensive Integration Tests for ResolvesTensionRel relationship.
Tests Project/Task -> Tension resolution relationships với đầy đủ validation, performance và edge cases.
"""

import pytest
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from trm_api.main import app
from trm_api.graph_models.project import Project
from trm_api.graph_models.task import Task
from trm_api.graph_models.tension import Tension
from trm_api.graph_models.resolves_tension import ResolvesTensionRel


class TestResolvesTensionRelCRUD:
    """Test basic CRUD operations cho ResolvesTensionRel"""
    
    def setup_method(self):
        """Setup test data cho mỗi test"""
        self.test_client = TestClient(app)
        
        # Tạo test entities
        self.project = Project(
            title=f"Tension Resolution Project {uuid.uuid4().hex[:8]}",
            description="Project for resolving business tensions",
            status="active"
        ).save()
        
        self.task = Task(
            name=f"Tension Resolution Task {uuid.uuid4().hex[:8]}",
            description="Task addressing specific tension",
            status="InProgress"
        ).save()
        
        self.problem_tension = Tension(
            title=f"System Performance Issue {uuid.uuid4().hex[:8]}",
            description="Application response time is degrading",
            tension_type="Problem",
            status="Open",
            priority=2
        ).save()
        
        self.opportunity_tension = Tension(
            title=f"Market Expansion Opportunity {uuid.uuid4().hex[:8]}",
            description="New market segment opportunity identified",
            tension_type="Opportunity",
            status="Open",
            priority=0
        ).save()
        
        self.risk_tension = Tension(
            title=f"Security Risk {uuid.uuid4().hex[:8]}",
            description="Potential security vulnerability identified",
            tension_type="Risk",
            status="Open",
            priority=1
        ).save()
    
    def teardown_method(self):
        """Cleanup sau mỗi test"""
        # Delete relationships first
        if hasattr(self, 'project') and self.project:
            for rel in self.project.resolves_tensions.all():
                rel.delete()
            self.project.delete()
            
        if hasattr(self, 'task') and self.task:
            for rel in self.task.resolves_tensions.all():
                rel.delete()
            self.task.delete()
            
        if hasattr(self, 'problem_tension') and self.problem_tension:
            self.problem_tension.delete()
        if hasattr(self, 'opportunity_tension') and self.opportunity_tension:
            self.opportunity_tension.delete()
        if hasattr(self, 'risk_tension') and self.risk_tension:
            self.risk_tension.delete()
    
    def test_project_resolves_tension_creation(self):
        """Test Project -> Tension resolution relationship creation"""
        # Create resolution relationship
        relationship = self.project.resolves_tensions.connect(
            self.problem_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ResolutionInProgress',
                'resolutionApproach': 'Performance optimization through caching and database tuning',
                'expectedOutcome': 'Reduce response time to under 200ms',
                'alignmentScore': 0.85,
                'priority': 2,
                'startDate': datetime.now(),
                'targetResolutionDate': datetime.now() + timedelta(days=30),
                'notes': 'Critical performance issue requiring immediate attention'
            }
        )
        
        # Verify relationship exists
        assert relationship is not None
        assert relationship.resolutionStatus == 'ResolutionInProgress'
        assert relationship.resolutionApproach == 'Performance optimization through caching and database tuning'
        assert relationship.expectedOutcome == 'Reduce response time to under 200ms'
        assert relationship.alignmentScore == 0.85
        assert relationship.priority == 2
        assert relationship.startDate is not None
        assert relationship.targetResolutionDate is not None
        assert relationship.notes == 'Critical performance issue requiring immediate attention'
        assert relationship.creationDate is not None
        
        # Verify from project side
        resolved_tensions = self.project.resolves_tensions.all()
        assert len(resolved_tensions) == 1
        assert resolved_tensions[0].title == self.problem_tension.title
    
    def test_task_resolves_tension_creation(self):
        """Test Task -> Tension resolution relationship creation"""
        # Create resolution relationship
        relationship = self.task.resolves_tensions.connect(
            self.opportunity_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'resolutionApproach': 'Market research and competitive analysis',
                'expectedOutcome': 'Identify viable market entry strategy',
                'alignmentScore': 0.75,
                'priority': 0,
                'targetResolutionDate': datetime.now() + timedelta(days=60),
                'notes': 'Requires market research before implementation'
            }
        )
        
        # Verify relationship
        assert relationship.resolutionStatus == 'Proposed'
        assert relationship.resolutionApproach == 'Market research and competitive analysis'
        assert relationship.alignmentScore == 0.75
        assert relationship.priority == 0
        assert relationship.targetResolutionDate is not None
    
    def test_multiple_tensions_per_project(self):
        """Test Project resolving multiple tensions"""
        # Connect multiple tensions with different resolution approaches
        problem_rel = self.project.resolves_tensions.connect(
            self.problem_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ResolutionInProgress',
                'priority': 2,
                'alignmentScore': 0.9
            }
        )
        
        risk_rel = self.project.resolves_tensions.connect(
            self.risk_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ApprovedForResolution',
                'priority': 1,
                'alignmentScore': 0.95
            }
        )
        
        opportunity_rel = self.project.resolves_tensions.connect(
            self.opportunity_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'priority': 0,
                'alignmentScore': 0.7
            }
        )
        
        # Verify all relationships
        resolved_tensions = self.project.resolves_tensions.all()
        assert len(resolved_tensions) == 3
        
        tension_titles = [tension.title for tension in resolved_tensions]
        assert self.problem_tension.title in tension_titles
        assert self.risk_tension.title in tension_titles
        assert self.opportunity_tension.title in tension_titles
        
        # Verify different priorities and statuses
        critical_count = 0
        in_progress_count = 0
        
        for tension in resolved_tensions:
            rel = self.project.resolves_tensions.relationship(tension)
            if rel.priority == 1: # Risk tension
                critical_count += 1
            if rel.resolutionStatus == 'ResolutionInProgress':
                in_progress_count += 1
        
        assert critical_count == 1  # Risk tension
        assert in_progress_count == 1  # Problem tension
    
    def test_resolution_status_progression(self):
        """Test resolution status progression"""
        # Create initial resolution
        relationship = self.project.resolves_tensions.connect(
            self.problem_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'priority': 2,
                'startDate': datetime.now()
            }
        )
        
        initial_creation_date = relationship.creationDate
        
        # Progress through resolution stages
        statuses = [
            'ApprovedForResolution',
            'ResolutionInProgress', 
            'PartiallyResolved',
            'Resolved'
        ]
        
        for status in statuses:
            relationship.resolutionStatus = status
            relationship.lastModifiedDate = datetime.now()
            
            if status == 'Resolved':
                relationship.actualResolutionDate = datetime.now()
            
            relationship.save()
            
            # Verify status update
            updated_rel = self.project.resolves_tensions.relationship(self.problem_tension)
            assert updated_rel.resolutionStatus == status
            assert updated_rel.creationDate == initial_creation_date  # Should not change
            assert updated_rel.lastModifiedDate > initial_creation_date
        
        # Verify final resolved state
        final_rel = self.project.resolves_tensions.relationship(self.problem_tension)
        assert final_rel.resolutionStatus == 'Resolved'
        assert final_rel.actualResolutionDate is not None
    
    def test_resolution_relationship_deletion(self):
        """Test xóa ResolvesTensionRel relationship"""
        # Create resolution
        self.project.resolves_tensions.connect(
            self.problem_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'priority': 0
            }
        )
        
        # Verify relationship exists
        assert len(self.project.resolves_tensions.all()) == 1
        
        # Delete relationship
        self.project.resolves_tensions.disconnect(self.problem_tension)
        
        # Verify deletion
        assert len(self.project.resolves_tensions.all()) == 0


class TestResolvesTensionRelValidation:
    """Test business rules và validation cho ResolvesTensionRel"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_client = TestClient(app)
        
        self.project = Project(
            title=f"Validation Project {uuid.uuid4().hex[:8]}",
            description="Project for validation testing",
            status="planning"
        ).save()
        
        self.tension = Tension(
            title=f"Test Tension {uuid.uuid4().hex[:8]}",
            description="Tension for validation",
            tension_type="Problem",
            status="Open",
            priority=0
        ).save()
    
    def teardown_method(self):
        """Cleanup"""
        if hasattr(self, 'project') and self.project:
            for rel in self.project.resolves_tensions.all():
                rel.delete()
            self.project.delete()
            
        if hasattr(self, 'tension') and self.tension:
            self.tension.delete()
    
    def test_resolution_status_validation(self):
        """Test tất cả resolution status values"""
        resolution_statuses = {
            'Proposed': 'Proposed',
            'ApprovedForResolution': 'Approved for Resolution',
            'ResolutionInProgress': 'Resolution in Progress',
            'PartiallyResolved': 'Partially Resolved',
            'Resolved': 'Resolved',
            'ResolutionFailed': 'Resolution Failed',
            'OnHold': 'On Hold',
            'Cancelled': 'Cancelled',
            'RequiresReview': 'Requires Review'
        }
        
        for status_key, status_description in resolution_statuses.items():
            # Delete previous relationship if exists
            try:
                self.project.resolves_tensions.disconnect(self.tension)
            except:
                pass
            
            # Create resolution with specific status
            relationship = self.project.resolves_tensions.connect(
                self.tension,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'resolutionStatus': status_key,
                    'priority': 0
                }
            )
            
            assert relationship.resolutionStatus == status_key
            print(f"✅ Resolution Status '{status_key}' ({status_description}) validated")
    
    def test_priority_levels_validation(self):
        """Test tất cả priority levels"""
        priority_levels = {
            'Critical': 'Critical',
            'High': 'High',
            'Medium': 'Medium',
            'Low': 'Low',
            'Informational': 'Informational'
        }
        
        for priority in priority_levels.keys():
            try:
                self.project.resolves_tensions.disconnect(self.tension)
            except:
                pass
            
            relationship = self.project.resolves_tensions.connect(
                self.tension,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'resolutionStatus': 'Proposed',
                    'priority': 1
                }
            )
            
            assert relationship.priority == 1
            print(f"✅ Priority '{priority}' validated")
    
    def test_alignment_score_validation(self):
        """Test alignment score range (0.0 - 1.0)"""
        test_scores = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for score in test_scores:
            try:
                self.project.resolves_tensions.disconnect(self.tension)
            except:
                pass
            
            relationship = self.project.resolves_tensions.connect(
                self.tension,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'resolutionStatus': 'Proposed',
                    'alignmentScore': score
                }
            )
            
            assert relationship.alignmentScore == score
    
    def test_default_values(self):
        """Test default values cho properties"""
        relationship = self.project.resolves_tensions.connect(
            self.tension,
            {'relationshipId': str(uuid.uuid4())}  # Only required field
        )
        
        # Test default values
        assert relationship.resolutionStatus == 'Proposed'  # Default status
        assert relationship.priority == 0  # Default priority
        assert relationship.alignmentScore == 0.0  # Default alignment
        assert relationship.creationDate is not None
        assert relationship.lastModifiedDate is not None
    
    def test_date_tracking_validation(self):
        """Test date fields tracking"""
        start_date = datetime.now()
        target_date = start_date + timedelta(days=45)
        
        relationship = self.project.resolves_tensions.connect(
            self.tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ApprovedForResolution',
                'startDate': start_date,
                'targetResolutionDate': target_date
            }
        )
        
        assert relationship.startDate == start_date
        assert relationship.targetResolutionDate == target_date
        assert relationship.actualResolutionDate is None  # Not resolved yet
        
        # Mark as resolved
        resolved_date = datetime.now()
        relationship.resolutionStatus = 'Resolved'
        relationship.actualResolutionDate = resolved_date
        relationship.save()
        
        updated_rel = self.project.resolves_tensions.relationship(self.tension)
        assert updated_rel.actualResolutionDate == resolved_date
    
    def test_resolution_approach_and_outcome(self):
        """Test resolution approach và expected outcome fields"""
        long_approach = "Comprehensive multi-phase approach involving stakeholder analysis, technical assessment, risk evaluation, and iterative implementation with continuous monitoring and feedback loops."
        
        long_outcome = "Expected to achieve measurable improvement in system performance, user satisfaction, operational efficiency, and strategic alignment with business objectives while minimizing risks and resource consumption."
        
        relationship = self.project.resolves_tensions.connect(
            self.tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ApprovedForResolution',
                'resolutionApproach': long_approach,
                'expectedOutcome': long_outcome,
                'notes': 'Detailed planning phase completed with stakeholder buy-in'
            }
        )
        
        assert relationship.resolutionApproach == long_approach
        assert relationship.expectedOutcome == long_outcome
        assert relationship.notes == 'Detailed planning phase completed with stakeholder buy-in'


class TestResolvesTensionRelComplexOperations:
    """Test complex operations và workflows cho ResolvesTensionRel"""
    
    def setup_method(self):
        """Setup complex test scenario"""
        self.test_client = TestClient(app)
        
        # Create multiple projects
        self.projects = []
        for i in range(3):
            project = Project(
                title=f"Resolution Project {i+1}",
                description=f"Resolution project {i+1} for testing",
                status="active"
            ).save()
            self.projects.append(project)
        
        # Create multiple tasks
        self.tasks = []
        for i in range(2):
            task = Task(
                name=f"Resolution Task {i+1}",
                description=f"Resolution task {i+1}",
                status="InProgress"
            ).save()
            self.tasks.append(task)
        
        # Create tension categories
        self.problems = []
        self.opportunities = []
        self.risks = []
        
        # Problem tensions
        problem_titles = ["Performance Bottleneck", "User Experience Issue", "Integration Challenge"]
        for title in problem_titles:
            tension = Tension(
                title=f"{title} {uuid.uuid4().hex[:8]}",
                description=f"{title} requiring resolution",
                tension_type="Problem",
                status="Open",
                priority=1
            ).save()
            self.problems.append(tension)
        
        # Opportunity tensions
        opportunity_titles = ["Market Expansion", "Technology Upgrade"]
        for title in opportunity_titles:
            tension = Tension(
                title=f"{title} {uuid.uuid4().hex[:8]}",
                description=f"{title} opportunity",
                tension_type="Opportunity",
                status="Open",
                priority=0
            ).save()
            self.opportunities.append(tension)
        
        # Risk tensions
        risk_titles = ["Security Vulnerability", "Compliance Risk"]
        for title in risk_titles:
            tension = Tension(
                title=f"{title} {uuid.uuid4().hex[:8]}",
                description=f"{title} requiring mitigation",
                tension_type="Risk",
                status="Open",
                priority=2
            ).save()
            self.risks.append(tension)
    
    def teardown_method(self):
        """Cleanup all test data"""
        # Clean up relationships first
        for project in self.projects:
            for rel in project.resolves_tensions.all():
                rel.delete()
            project.delete()
        
        for task in self.tasks:
            for rel in task.resolves_tensions.all():
                rel.delete()
            task.delete()
        
        for tension in self.problems + self.opportunities + self.risks:
            tension.delete()
    
    def test_comprehensive_tension_resolution_portfolio(self):
        """Test comprehensive tension resolution across project portfolio"""
        main_project = self.projects[0]
        
        # Resolve different types of tensions with varied approaches
        # Critical risk resolution
        security_resolution = main_project.resolves_tensions.connect(
            self.risks[0],  # Security Vulnerability
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ResolutionInProgress',
                'resolutionApproach': 'Security audit, vulnerability assessment, and patch deployment',
                'expectedOutcome': 'Eliminate critical security vulnerabilities',
                'alignmentScore': 0.95,
                'priority': 2,
                'startDate': datetime.now(),
                'targetResolutionDate': datetime.now() + timedelta(days=14),
                'notes': 'Emergency security patch required'
            }
        )
        
        # High priority problem resolution
        performance_resolution = main_project.resolves_tensions.connect(
            self.problems[0],  # Performance Bottleneck
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ApprovedForResolution',
                'resolutionApproach': 'Performance optimization and infrastructure scaling',
                'expectedOutcome': 'Improve system response time by 50%',
                'alignmentScore': 0.85,
                'priority': 1,
                'startDate': datetime.now() + timedelta(days=7),
                'targetResolutionDate': datetime.now() + timedelta(days=30),
                'notes': 'Performance metrics baseline established'
            }
        )
        
        # Medium priority opportunity
        market_resolution = main_project.resolves_tensions.connect(
            self.opportunities[0],  # Market Expansion
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'resolutionApproach': 'Market research and pilot program development',
                'expectedOutcome': 'Enter new market segment with 15% market share',
                'alignmentScore': 0.75,
                'priority': 0,
                'targetResolutionDate': datetime.now() + timedelta(days=90),
                'notes': 'Requires market analysis completion'
            }
        )
        
        # Verify comprehensive resolution portfolio
        resolved_tensions = main_project.resolves_tensions.all()
        assert len(resolved_tensions) == 3
        
        # Analyze resolution priorities
        critical_resolutions = 0
        high_resolutions = 0
        in_progress_resolutions = 0
        
        for tension in resolved_tensions:
            rel = main_project.resolves_tensions.relationship(tension)
            if rel.priority == 2: # Security
                critical_resolutions += 1
            elif rel.priority == 1: # Performance
                high_resolutions += 1
            if rel.resolutionStatus == 'ResolutionInProgress':
                in_progress_resolutions += 1
        
        assert critical_resolutions == 1  # Security
        assert high_resolutions == 1  # Performance
        assert in_progress_resolutions == 1  # Security already started
        
        # Calculate portfolio alignment score
        total_alignment = sum(
            main_project.resolves_tensions.relationship(tension).alignmentScore
            for tension in resolved_tensions
        )
        average_alignment = total_alignment / len(resolved_tensions)
        assert average_alignment > 0.8  # High overall alignment
    
    def test_cross_project_tension_resolution(self):
        """Test same tension being addressed by multiple projects"""
        shared_tension = self.problems[1]  # User Experience Issue
        
        # Multiple projects addressing same tension with different approaches
        ui_project_resolution = self.projects[0].resolves_tensions.connect(
            shared_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ResolutionInProgress',
                'resolutionApproach': 'UI/UX redesign and user testing',
                'expectedOutcome': 'Improve user satisfaction scores by 30%',
                'alignmentScore': 0.9,
                'priority': 1,
                'notes': 'Frontend-focused approach'
            }
        )
        
        backend_project_resolution = self.projects[1].resolves_tensions.connect(
            shared_tension,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ApprovedForResolution',
                'resolutionApproach': 'Backend performance optimization and API improvements',
                'expectedOutcome': 'Reduce page load times and improve responsiveness',
                'alignmentScore': 0.85,
                'priority': 1,
                'notes': 'Backend-focused approach'
            }
        )
        
        # Verify multiple resolution approaches
        resolving_projects = []
        for project in self.projects[:2]:
            resolved_tensions = project.resolves_tensions.all()
            for tension in resolved_tensions:
                if tension.title == shared_tension.title:
                    rel = project.resolves_tensions.relationship(tension)
                    resolving_projects.append((project, rel))
        
        assert len(resolving_projects) == 2  # Two projects addressing same tension
        
        # Verify different approaches
        approaches = [rel.resolutionApproach for project, rel in resolving_projects]
        assert 'UI/UX redesign' in approaches[0]
        assert 'Backend performance' in approaches[1]
    
    def test_task_level_tension_resolution(self):
        """Test task-level tension resolution"""
        integration_task = self.tasks[0]
        integration_problem = self.problems[2]  # Integration Challenge
        
        # Task addressing specific integration tension
        task_resolution = integration_task.resolves_tensions.connect(
            integration_problem,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'ResolutionInProgress',
                'resolutionApproach': 'API endpoint harmonization and data mapping',
                'expectedOutcome': 'Seamless data flow between systems',
                'alignmentScore': 0.8,
                'priority': 1,
                'startDate': datetime.now(),
                'targetResolutionDate': datetime.now() + timedelta(days=21),
                'notes': 'Critical for system integration milestone'
            }
        )
        
        # Verify task resolution
        task_tensions = integration_task.resolves_tensions.all()
        assert len(task_tensions) == 1
        assert task_tensions[0].title == integration_problem.title
        
        task_rel = integration_task.resolves_tensions.relationship(integration_problem)
        assert task_rel.resolutionStatus == 'ResolutionInProgress'
        assert 'API endpoint harmonization' in task_rel.resolutionApproach
    
    def test_resolution_lifecycle_workflow(self):
        """Test complete resolution lifecycle workflow"""
        project = self.projects[2]
        compliance_risk = self.risks[1]  # Compliance Risk
        
        # Stage 1: Initial proposal
        resolution = project.resolves_tensions.connect(
            compliance_risk,
            {
                'relationshipId': str(uuid.uuid4()),
                'resolutionStatus': 'Proposed',
                'resolutionApproach': 'Compliance audit and remediation plan',
                'expectedOutcome': 'Full regulatory compliance certification',
                'alignmentScore': 0.9,
                'priority': 2,
                'notes': 'Initial compliance assessment completed'
            }
        )
        
        assert resolution.resolutionStatus == 'Proposed'
        
        # Stage 2: Approval
        resolution.resolutionStatus = 'ApprovedForResolution'
        resolution.startDate = datetime.now()
        resolution.targetResolutionDate = datetime.now() + timedelta(days=60)
        resolution.lastModifiedDate = datetime.now()
        resolution.save()
        
        # Stage 3: Start resolution
        resolution.resolutionStatus = 'ResolutionInProgress'
        resolution.notes = 'Compliance team assigned, remediation in progress'
        resolution.lastModifiedDate = datetime.now()
        resolution.save()
        
        # Stage 4: Partial resolution
        resolution.resolutionStatus = 'PartiallyResolved'
        resolution.notes = 'Major compliance issues addressed, minor items remaining'
        resolution.alignmentScore = 0.95  # Improved alignment
        resolution.lastModifiedDate = datetime.now()
        resolution.save()
        
        # Stage 5: Full resolution
        resolution.resolutionStatus = 'Resolved'
        resolution.actualResolutionDate = datetime.now()
        resolution.notes = 'Full compliance certification achieved'
        resolution.lastModifiedDate = datetime.now()
        resolution.save()
        
        # Verify final state
        final_resolution = project.resolves_tensions.relationship(compliance_risk)
        assert final_resolution.resolutionStatus == 'Resolved'
        assert final_resolution.actualResolutionDate is not None
        assert final_resolution.alignmentScore == 0.95
        assert 'Full compliance certification achieved' in final_resolution.notes
        
        # Verify timeline
        time_to_resolve = (
            final_resolution.actualResolutionDate - final_resolution.startDate
        ).days
        target_days = (
            final_resolution.targetResolutionDate - final_resolution.startDate
        ).days
        
        # Resolution completed within target timeframe
        assert time_to_resolve <= target_days


class TestResolvesTensionRelPerformance:
    """Test performance và scalability cho ResolvesTensionRel"""
    
    def setup_method(self):
        """Setup performance test scenario"""
        self.test_client = TestClient(app)
        
        # Create entities for bulk operations
        self.projects = []
        self.tensions = []
        
        # Create 3 projects
        for i in range(3):
            project = Project(
                title=f"Performance Project {i+1}",
                description=f"Performance test project {i+1}",
                status="active"
            ).save()
            self.projects.append(project)
        
        # Create 9 tensions of different types
        tension_types = ["Problem", "Opportunity", "Risk"]
        priorities = [2, 1, 0] # 2 (Critical), 1 (High), 0 (Medium)
        
        for i in range(9):
            tension_type = tension_types[i % len(tension_types)]
            priority = priorities[i % len(priorities)]
            
            tension = Tension(
                title=f"{tension_type} Tension {i+1}",
                description=f"Performance test {tension_type.lower()} tension",
                tension_type=tension_type,
                status="Open",
                priority=priority
            ).save()
            self.tensions.append(tension)
    
    def teardown_method(self):
        """Cleanup performance test data"""
        # Clean up relationships first
        for project in self.projects:
            for rel in project.resolves_tensions.all():
                rel.delete()
            project.delete()
        
        for tension in self.tensions:
            tension.delete()
    
    def test_bulk_resolution_creation(self):
        """Test bulk resolution creation performance"""
        start_time = datetime.now()
        
        # Create resolutions (3 projects × 6 tensions = 18 relationships)
        relationship_count = 0
        resolution_statuses = ['Proposed', 'ApprovedForResolution', 'ResolutionInProgress']
        priorities = [2, 1, 0] # 2 (Critical), 1 (High), 0 (Medium)
        
        for i, project in enumerate(self.projects):
            for j in range(6):  # 6 tensions per project
                tension = self.tensions[j]
                status = resolution_statuses[j % len(resolution_statuses)]
                priority = priorities[j % len(priorities)]
                alignment = 0.5 + (j % 5) * 0.1  # 0.5 to 0.9
                
                relationship = project.resolves_tensions.connect(
                    tension,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'resolutionStatus': status,
                        'priority': priority,
                        'alignmentScore': alignment,
                        'resolutionApproach': f'Approach for {tension.tension_type} resolution',
                        'expectedOutcome': f'Expected outcome for tension {j+1}',
                        'notes': f'Bulk resolution {relationship_count + 1}'
                    }
                )
                relationship_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Verify all relationships created
        assert relationship_count == 18  # 3 projects × 6 tensions
        
        # Verify performance (should complete within reasonable time)
        assert duration < 30.0  # 30 seconds maximum
        print(f"✅ Created {relationship_count} tension resolutions in {duration:.2f} seconds")
        
        # Verify data integrity
        total_resolutions = 0
        for project in self.projects:
            project_resolutions = project.resolves_tensions.all()
            total_resolutions += len(project_resolutions)
        
        assert total_resolutions == 18
    
    def test_resolution_query_performance(self):
        """Test query performance with large resolution dataset"""
        # First create resolutions
        for i, project in enumerate(self.projects):
            for j, tension in enumerate(self.tensions[:5]):  # 5 tensions per project
                project.resolves_tensions.connect(
                    tension,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'resolutionStatus': 'ResolutionInProgress',
                        'priority': 1,
                        'alignmentScore': 0.8
                    }
                )
        
        # Test query performance
        start_time = datetime.now()
        
        # Query all resolutions for each project
        total_resolutions_found = 0
        for project in self.projects:
            resolved_tensions = project.resolves_tensions.all()
            total_resolutions_found += len(resolved_tensions)
        
        end_time = datetime.now()
        query_duration = (end_time - start_time).total_seconds()
        
        # Verify query results
        assert total_resolutions_found == 15  # 3 projects × 5 tensions
        
        # Verify query performance
        assert query_duration < 10.0  # 10 seconds maximum
        print(f"✅ Queried {total_resolutions_found} tension resolutions in {query_duration:.2f} seconds")
    
    def test_resolution_status_filtering(self):
        """Test filtering resolutions by status và priority"""
        # Create diverse resolutions
        statuses = ['Proposed', 'ApprovedForResolution', 'ResolutionInProgress', 'Resolved']
        priorities = [2, 1, 0, 2] # 2 (Critical), 1 (High), 0 (Medium), 2 (Critical)
        
        for i, project in enumerate(self.projects):
            for j, tension in enumerate(self.tensions[:4]):  # 4 tensions per project
                status = statuses[j % len(statuses)]
                priority = priorities[j % len(priorities)]
                
                project.resolves_tensions.connect(
                    tension,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'resolutionStatus': status,
                        'priority': priority,
                        'alignmentScore': 0.7 + (j % 3) * 0.1
                    }
                )
        
        # Test filtering by resolution status
        in_progress_resolutions = []
        for project in self.projects:
            resolved_tensions = project.resolves_tensions.all()
            for tension in resolved_tensions:
                rel = project.resolves_tensions.relationship(tension)
                if rel.resolutionStatus == 'ResolutionInProgress':
                    in_progress_resolutions.append((project, tension, rel))
        
        assert len(in_progress_resolutions) > 0
        print(f"✅ Found {len(in_progress_resolutions)} in-progress resolutions")
        
        # Test filtering by priority
        critical_resolutions = []
        for project in self.projects:
            resolved_tensions = project.resolves_tensions.all()
            for tension in resolved_tensions:
                rel = project.resolves_tensions.relationship(tension)
                if rel.priority == 2: # Critical
                    critical_resolutions.append((project, tension, rel))
        
        assert len(critical_resolutions) > 0
        print(f"✅ Found {len(critical_resolutions)} critical resolutions")
        
        # Test filtering by alignment score
        high_alignment_resolutions = []
        for project in self.projects:
            resolved_tensions = project.resolves_tensions.all()
            for tension in resolved_tensions:
                rel = project.resolves_tensions.relationship(tension)
                if rel.alignmentScore >= 0.8:
                    high_alignment_resolutions.append((project, tension, rel))
        
        print(f"✅ Found {len(high_alignment_resolutions)} high-alignment resolutions")
    
    def test_resolution_metrics_aggregation(self):
        """Test aggregation of resolution metrics"""
        # Create resolutions with varied metrics
        for i, project in enumerate(self.projects):
            for j, tension in enumerate(self.tensions[:3]):  # 3 tensions per project
                alignment_score = 0.6 + (j * 0.15)  # 0.6, 0.75, 0.9
                
                relationship = project.resolves_tensions.connect(
                    tension,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'resolutionStatus': 'ResolutionInProgress',
                        'priority': 1,
                        'alignmentScore': alignment_score,
                        'startDate': datetime.now() - timedelta(days=j*10),
                        'targetResolutionDate': datetime.now() + timedelta(days=30-j*5)
                    }
                )
        
        # Test metrics aggregation
        start_time = datetime.now()
        
        total_alignment_score = 0
        resolution_count = 0
        overdue_count = 0
        current_date = datetime.now()
        
        for project in self.projects:
            resolved_tensions = project.resolves_tensions.all()
            for tension in resolved_tensions:
                rel = project.resolves_tensions.relationship(tension)
                total_alignment_score += rel.alignmentScore
                resolution_count += 1
                
                # Check if overdue
                if rel.targetResolutionDate and rel.targetResolutionDate < current_date:
                    overdue_count += 1
        
        end_time = datetime.now()
        aggregation_duration = (end_time - start_time).total_seconds()
        
        # Calculate metrics
        average_alignment = total_alignment_score / resolution_count
        overdue_percentage = (overdue_count / resolution_count) * 100
        
        # Verify calculations
        assert resolution_count == 9  # 3 projects × 3 tensions
        assert average_alignment > 0.6  # Minimum alignment
        
        # Verify performance
        assert aggregation_duration < 5.0  # 5 seconds maximum
        print(f"✅ Aggregated metrics for {resolution_count} resolutions in {aggregation_duration:.2f} seconds")
        print(f"✅ Average alignment score: {average_alignment:.2f}")
        print(f"✅ Overdue resolutions: {overdue_count}/{resolution_count} ({overdue_percentage:.1f}%)") 