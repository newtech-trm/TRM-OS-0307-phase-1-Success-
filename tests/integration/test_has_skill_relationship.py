"""
Comprehensive Integration Tests for HasSkillRel relationship.
Tests Agent/User -> Skill relationships với đầy đủ validation, performance và edge cases.
"""

import pytest
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from trm_api.main import app
from trm_api.graph_models.agent import Agent
from trm_api.graph_models.user import User
from trm_api.graph_models.skill import GraphSkill
from trm_api.graph_models.has_skill import HasSkillRel


class TestHasSkillRelCRUD:
    """Test basic CRUD operations cho HasSkillRel"""
    
    def setup_method(self):
        """Setup test data cho mỗi test"""
        self.test_client = TestClient(app)
        
        # Tạo test entities
        self.agent = Agent(
            name="Python Developer Agent",
            description="AI agent specialized in Python development",
            agent_type="AIAgent",
            status="active"
        ).save()
        
        self.user = User(
            username=f"test_user_{uuid.uuid4().hex[:8]}",
            email=f"test_{uuid.uuid4().hex[:8]}@example.com",
            full_name="Test User"
        ).save()
        
        self.skill = GraphSkill(
            name=f"Python Programming {uuid.uuid4().hex[:8]}",
            description="Programming language skill",
            category="programming"
        ).save()
        
        self.advanced_skill = GraphSkill(
            name=f"Machine Learning {uuid.uuid4().hex[:8]}",
            description="AI/ML expertise",
            category="ai"
        ).save()
    
    def teardown_method(self):
        """Cleanup sau mỗi test"""
        # Delete relationships first
        if hasattr(self, 'agent') and self.agent:
            for rel in self.agent.has_skills.all():
                rel.delete()
            self.agent.delete()
            
        if hasattr(self, 'user') and self.user:
            for rel in self.user.has_skills.all():
                rel.delete()
            self.user.delete()
            
        if hasattr(self, 'skill') and self.skill:
            self.skill.delete()
            
        if hasattr(self, 'advanced_skill') and self.advanced_skill:
            self.advanced_skill.delete()
    
    def test_agent_has_skill_creation(self):
        """Test Agent -> Skill relationship creation"""
        # Create relationship
        relationship = self.agent.has_skills.connect(
            self.skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 4,  # Proficient
                'confidenceScore': 0.85,
                'endorsementCount': 5,
                'yearsExperience': 3.5,
                'notes': "Strong Python skills with web frameworks"
            }
        )
        
        # Verify relationship exists
        assert relationship is not None
        assert relationship.proficiencyLevel == 4
        assert relationship.confidenceScore == 0.85
        assert relationship.endorsementCount == 5
        assert relationship.yearsExperience == 3.5
        assert relationship.notes == "Strong Python skills with web frameworks"
        assert relationship.creationDate is not None
        
        # Verify from agent side
        agent_skills = self.agent.has_skills.all()
        assert len(agent_skills) == 1
        assert agent_skills[0].name == self.skill.name
    
    def test_user_has_skill_creation(self):
        """Test User -> Skill relationship creation"""
        # Create relationship
        relationship = self.user.has_skills.connect(
            self.skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 3,  # Competent
                'confidenceScore': 0.75,
                'endorsementCount': 2,
                'yearsExperience': 2.0,
                'lastUsed': datetime.now() - timedelta(days=30),
                'preferenceRank': 1,
                'notes': "Primary programming language"
            }
        )
        
        # Verify relationship
        assert relationship.proficiencyLevel == 3
        assert relationship.confidenceScore == 0.75
        assert relationship.preferenceRank == 1
        assert relationship.lastUsed is not None
        
        # Verify from skill side
        skilled_users = self.skill.skilled_users.all()
        assert len(skilled_users) == 1
        assert skilled_users[0].username == self.user.username
    
    def test_multiple_skills_per_agent(self):
        """Test Agent có nhiều skills"""
        # Connect multiple skills
        rel1 = self.agent.has_skills.connect(
            self.skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 4,
                'preferenceRank': 1
            }
        )
        
        rel2 = self.agent.has_skills.connect(
            self.advanced_skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 3,
                'preferenceRank': 2
            }
        )
        
        # Verify both relationships
        agent_skills = self.agent.has_skills.all()
        assert len(agent_skills) == 2
        
        skill_names = [skill.name for skill in agent_skills]
        assert self.skill.name in skill_names
        assert self.advanced_skill.name in skill_names
    
    def test_skill_relationship_update(self):
        """Test update HasSkillRel properties"""
        # Create initial relationship
        relationship = self.agent.has_skills.connect(
            self.skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 2,  # Advanced Beginner
                'confidenceScore': 0.6,
                'endorsementCount': 1
            }
        )
        
        initial_creation_date = relationship.creationDate
        
        # Update relationship properties
        relationship.proficiencyLevel = 4  # Proficient
        relationship.confidenceScore = 0.9
        relationship.endorsementCount = 8
        relationship.lastModifiedDate = datetime.now()
        relationship.save()
        
        # Verify updates
        updated_rel = self.agent.has_skills.relationship(self.skill)
        assert updated_rel.proficiencyLevel == 4
        assert updated_rel.confidenceScore == 0.9
        assert updated_rel.endorsementCount == 8
        assert updated_rel.creationDate == initial_creation_date  # Should not change
        assert updated_rel.lastModifiedDate > initial_creation_date
    
    def test_relationship_deletion(self):
        """Test xóa HasSkillRel relationship"""
        # Create relationship
        self.agent.has_skills.connect(
            self.skill,
            {'relationshipId': str(uuid.uuid4()), 'proficiencyLevel': 3}
        )
        
        # Verify relationship exists
        assert len(self.agent.has_skills.all()) == 1
        
        # Delete relationship
        self.agent.has_skills.disconnect(self.skill)
        
        # Verify deletion
        assert len(self.agent.has_skills.all()) == 0
        assert len(self.skill.skilled_agents.all()) == 0


class TestHasSkillRelValidation:
    """Test business rules và validation cho HasSkillRel"""
    
    def setup_method(self):
        """Setup test data"""
        self.test_client = TestClient(app)
        
        self.agent = Agent(
            name="Test Agent",
            description="Test agent",
            agent_type="AIAgent",
            status="active"
        ).save()
        
        self.skill = GraphSkill(
            name=f"Test Skill {uuid.uuid4().hex[:8]}",
            description="Test skill",
            category="test"
        ).save()
    
    def teardown_method(self):
        """Cleanup"""
        if hasattr(self, 'agent') and self.agent:
            for rel in self.agent.has_skills.all():
                rel.delete()
            self.agent.delete()
            
        if hasattr(self, 'skill') and self.skill:
            self.skill.delete()
    
    def test_proficiency_level_validation(self):
        """Test tất cả proficiency levels (1-5)"""
        proficiency_levels = {
            1: 'Novice',
            2: 'Advanced Beginner',
            3: 'Competent',
            4: 'Proficient',
            5: 'Expert'
        }
        
        for level, description in proficiency_levels.items():
            # Delete previous relationship if exists
            try:
                self.agent.has_skills.disconnect(self.skill)
            except:
                pass
            
            # Create relationship with specific proficiency level
            relationship = self.agent.has_skills.connect(
                self.skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': level
                }
            )
            
            assert relationship.proficiencyLevel == level
            print(f"✅ Proficiency Level {level} ({description}) validated")
    
    def test_confidence_score_boundaries(self):
        """Test confidence score boundaries (0.0 - 1.0)"""
        test_scores = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for score in test_scores:
            try:
                self.agent.has_skills.disconnect(self.skill)
            except:
                pass
            
            relationship = self.agent.has_skills.connect(
                self.skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': 3,
                    'confidenceScore': score
                }
            )
            
            assert relationship.confidenceScore == score
    
    def test_default_values(self):
        """Test default values cho optional properties"""
        relationship = self.agent.has_skills.connect(
            self.skill,
            {'relationshipId': str(uuid.uuid4())}  # Only required fields
        )
        
        # Test default values
        assert relationship.proficiencyLevel == 1  # Default Novice
        assert relationship.confidenceScore == 0.5  # Default confidence
        assert relationship.endorsementCount == 0  # Default endorsements
        assert relationship.creationDate is not None
        assert relationship.lastModifiedDate is not None
    
    def test_required_relationship_id(self):
        """Test relationshipId là required"""
        # Tạo relationship mà không có relationshipId sẽ lỗi
        with pytest.raises(Exception):
            self.agent.has_skills.connect(
                self.skill,
                {'proficiencyLevel': 3}  # Missing relationshipId
            )
    
    def test_years_experience_validation(self):
        """Test yearsExperience values"""
        experience_values = [0.5, 1.0, 5.5, 10.0, 20.5]
        
        for experience in experience_values:
            try:
                self.agent.has_skills.disconnect(self.skill)
            except:
                pass
            
            relationship = self.agent.has_skills.connect(
                self.skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': 3,
                    'yearsExperience': experience
                }
            )
            
            assert relationship.yearsExperience == experience


class TestHasSkillRelComplexOperations:
    """Test complex operations và workflows cho HasSkillRel"""
    
    def setup_method(self):
        """Setup complex test scenario"""
        self.test_client = TestClient(app)
        
        # Create multiple agents
        self.agents = []
        for i in range(3):
            agent = Agent(
                name=f"Agent {i+1}",
                description=f"Test agent {i+1}",
                agent_type="AIAgent",
                status="active"
            ).save()
            self.agents.append(agent)
        
        # Create multiple users
        self.users = []
        for i in range(2):
            user = User(
                username=f"user_{i+1}_{uuid.uuid4().hex[:8]}",
                email=f"user{i+1}@example.com",
                full_name=f"User {i+1}"
            ).save()
            self.users.append(user)
        
        # Create skill categories
        self.programming_skills = []
        self.management_skills = []
        
        prog_skills = ["Python", "JavaScript", "Java", "Go"]
        mgmt_skills = ["Project Management", "Team Leadership", "Strategy"]
        
        for skill_name in prog_skills:
            skill = GraphSkill(
                name=f"{skill_name} {uuid.uuid4().hex[:8]}",
                description=f"{skill_name} expertise",
                category="programming"
            ).save()
            self.programming_skills.append(skill)
        
        for skill_name in mgmt_skills:
            skill = GraphSkill(
                name=f"{skill_name} {uuid.uuid4().hex[:8]}",
                description=f"{skill_name} expertise",
                category="management"
            ).save()
            self.management_skills.append(skill)
    
    def teardown_method(self):
        """Cleanup all test data"""
        # Clean up relationships first
        for agent in self.agents:
            for rel in agent.has_skills.all():
                rel.delete()
            agent.delete()
        
        for user in self.users:
            for rel in user.has_skills.all():
                rel.delete()
            user.delete()
        
        for skill in self.programming_skills + self.management_skills:
            skill.delete()
    
    def test_skill_portfolio_assignment(self):
        """Test assign skill portfolio cho agents"""
        agent = self.agents[0]
        
        # Assign programming skills với different proficiency levels
        for i, skill in enumerate(self.programming_skills):
            proficiency = min(5, i + 2)  # 2, 3, 4, 5
            preference = i + 1
            
            relationship = agent.has_skills.connect(
                skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': proficiency,
                    'confidenceScore': 0.7 + (i * 0.1),
                    'preferenceRank': preference,
                    'yearsExperience': float(i + 1),
                    'notes': f"Skill level {proficiency} in {skill.name}"
                }
            )
        
        # Verify portfolio
        agent_skills = agent.has_skills.all()
        assert len(agent_skills) == len(self.programming_skills)
        
        # Verify proficiency progression
        for skill in agent_skills:
            rel = agent.has_skills.relationship(skill)
            assert rel.proficiencyLevel >= 2
            assert rel.proficiencyLevel <= 5
            assert rel.confidenceScore >= 0.7
    
    def test_cross_entity_skill_sharing(self):
        """Test same skill across multiple agents và users"""
        target_skill = self.programming_skills[0]  # Python skill
        
        # Assign same skill to multiple agents với different levels
        for i, agent in enumerate(self.agents):
            proficiency = i + 3  # 3, 4, 5
            relationship = agent.has_skills.connect(
                target_skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': proficiency,
                    'confidenceScore': 0.6 + (i * 0.15),
                    'endorsementCount': i * 2,
                    'yearsExperience': float(i + 2)
                }
            )
        
        # Assign same skill to users
        for i, user in enumerate(self.users):
            relationship = user.has_skills.connect(
                target_skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': 4,  # All users proficient
                    'confidenceScore': 0.8,
                    'endorsementCount': 5,
                    'preferenceRank': 1
                }
            )
        
        # Verify skill distribution
        skilled_agents = target_skill.skilled_agents.all()
        skilled_users = target_skill.skilled_users.all()
        
        assert len(skilled_agents) == len(self.agents)
        assert len(skilled_users) == len(self.users)
        
        # Verify different proficiency levels among agents
        agent_proficiencies = []
        for agent in skilled_agents:
            rel = agent.has_skills.relationship(target_skill)
            agent_proficiencies.append(rel.proficiencyLevel)
        
        assert len(set(agent_proficiencies)) > 1  # Different levels
    
    def test_skill_preference_ranking(self):
        """Test skill preference ranking system"""
        agent = self.agents[0]
        
        # Assign skills với explicit preference ranking
        skills_with_prefs = [
            (self.programming_skills[0], 1, "Primary skill"),
            (self.programming_skills[1], 2, "Secondary skill"),
            (self.management_skills[0], 3, "Leadership skill"),
            (self.programming_skills[2], 4, "Backup skill")
        ]
        
        for skill, pref_rank, note in skills_with_prefs:
            relationship = agent.has_skills.connect(
                skill,
                {
                    'relationshipId': str(uuid.uuid4()),
                    'proficiencyLevel': 4,
                    'preferenceRank': pref_rank,
                    'notes': note
                }
            )
        
        # Verify preference ordering
        agent_skills = agent.has_skills.all()
        assert len(agent_skills) == 4
        
        # Check if we can retrieve skills by preference
        for skill in agent_skills:
            rel = agent.has_skills.relationship(skill)
            assert rel.preferenceRank in [1, 2, 3, 4]
            assert rel.notes is not None
    
    def test_skill_endorsement_tracking(self):
        """Test endorsement count tracking"""
        agent = self.agents[0]
        skill = self.programming_skills[0]
        
        # Create initial relationship
        relationship = agent.has_skills.connect(
            skill,
            {
                'relationshipId': str(uuid.uuid4()),
                'proficiencyLevel': 3,
                'endorsementCount': 0
            }
        )
        
        # Simulate endorsement increases
        endorsement_progression = [1, 3, 5, 8, 12]
        
        for endorsement_count in endorsement_progression:
            relationship.endorsementCount = endorsement_count
            relationship.lastModifiedDate = datetime.now()
            relationship.save()
            
            # Verify update
            updated_rel = agent.has_skills.relationship(skill)
            assert updated_rel.endorsementCount == endorsement_count
        
        # Final verification
        final_rel = agent.has_skills.relationship(skill)
        assert final_rel.endorsementCount == 12


class TestHasSkillRelPerformance:
    """Test performance và scalability cho HasSkillRel"""
    
    def setup_method(self):
        """Setup performance test scenario"""
        self.test_client = TestClient(app)
        
        # Create entities for bulk operations
        self.agents = []
        self.skills = []
        
        # Create 5 agents
        for i in range(5):
            agent = Agent(
                name=f"Perf Agent {i+1}",
                description=f"Performance test agent {i+1}",
                agent_type="AIAgent",
                status="active"
            ).save()
            self.agents.append(agent)
        
        # Create 10 skills
        skill_categories = ["programming", "management", "design", "data", "devops"]
        for i in range(10):
            category = skill_categories[i % len(skill_categories)]
            skill = GraphSkill(
                name=f"Skill {i+1} {uuid.uuid4().hex[:8]}",
                description=f"Performance test skill {i+1}",
                category=category
            ).save()
            self.skills.append(skill)
    
    def teardown_method(self):
        """Cleanup performance test data"""
        # Clean up relationships first
        for agent in self.agents:
            for rel in agent.has_skills.all():
                rel.delete()
            agent.delete()
        
        for skill in self.skills:
            skill.delete()
    
    def test_bulk_skill_assignment(self):
        """Test bulk skill assignment performance"""
        start_time = datetime.now()
        
        # Assign all skills to all agents (5 agents × 10 skills = 50 relationships)
        relationship_count = 0
        
        for agent in self.agents:
            for i, skill in enumerate(self.skills):
                proficiency = (i % 5) + 1  # Cycle through 1-5
                confidence = 0.5 + (i % 5) * 0.1  # 0.5, 0.6, 0.7, 0.8, 0.9
                
                relationship = agent.has_skills.connect(
                    skill,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'proficiencyLevel': proficiency,
                        'confidenceScore': confidence,
                        'endorsementCount': i % 10,
                        'yearsExperience': float(i % 8 + 1)
                    }
                )
                relationship_count += 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Verify all relationships created
        assert relationship_count == 50  # 5 agents × 10 skills
        
        # Verify performance (should complete within reasonable time)
        assert duration < 30.0  # 30 seconds maximum
        print(f"✅ Created {relationship_count} relationships in {duration:.2f} seconds")
        
        # Verify data integrity
        for agent in self.agents:
            agent_skills = agent.has_skills.all()
            assert len(agent_skills) == 10  # Each agent has all 10 skills
    
    def test_skill_query_performance(self):
        """Test query performance với large relationship set"""
        # First create relationships
        for agent in self.agents[:3]:  # Use 3 agents
            for skill in self.skills[:5]:  # Use 5 skills
                agent.has_skills.connect(
                    skill,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'proficiencyLevel': 4,
                        'confidenceScore': 0.8
                    }
                )
        
        # Test query performance
        start_time = datetime.now()
        
        # Query all skills for each agent
        total_skills_found = 0
        for agent in self.agents[:3]:
            agent_skills = agent.has_skills.all()
            total_skills_found += len(agent_skills)
        
        # Query all agents for each skill
        total_agents_found = 0
        for skill in self.skills[:5]:
            skilled_agents = skill.skilled_agents.all()
            total_agents_found += len(skilled_agents)
        
        end_time = datetime.now()
        query_duration = (end_time - start_time).total_seconds()
        
        # Verify query results
        assert total_skills_found == 15  # 3 agents × 5 skills
        assert total_agents_found == 15  # 5 skills × 3 agents
        
        # Verify query performance
        assert query_duration < 10.0  # 10 seconds maximum
        print(f"✅ Queried {total_skills_found + total_agents_found} relationships in {query_duration:.2f} seconds")
    
    def test_skill_filtering_and_search(self):
        """Test filtering skills by proficiency và category"""
        # Create diverse skill assignments
        for i, agent in enumerate(self.agents):
            for j, skill in enumerate(self.skills):
                proficiency = ((i + j) % 5) + 1  # Varied proficiency levels
                category_bonus = 0.1 if skill.category == "programming" else 0.0
                
                agent.has_skills.connect(
                    skill,
                    {
                        'relationshipId': str(uuid.uuid4()),
                        'proficiencyLevel': proficiency,
                        'confidenceScore': 0.6 + category_bonus,
                        'preferenceRank': j + 1
                    }
                )
        
        # Test filtering expert level skills (proficiency = 5)
        expert_agents = []
        for agent in self.agents:
            agent_skills = agent.has_skills.all()
            for skill in agent_skills:
                rel = agent.has_skills.relationship(skill)
                if rel.proficiencyLevel == 5:
                    expert_agents.append((agent, skill, rel))
        
        assert len(expert_agents) > 0  # Should find some expert relationships
        print(f"✅ Found {len(expert_agents)} expert-level skill relationships")
        
        # Test filtering by skill category
        programming_skills_count = 0
        for skill in self.skills:
            if skill.category == "programming":
                skilled_agents = skill.skilled_agents.all()
                programming_skills_count += len(skilled_agents)
        
        assert programming_skills_count > 0
        print(f"✅ Found {programming_skills_count} programming skill assignments") 