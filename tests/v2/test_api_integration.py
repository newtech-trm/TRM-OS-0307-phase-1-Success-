#!/usr/bin/env python3
"""
Integration Tests for TRM-OS v2 API
===================================

Test integration của conversational intelligence v2 với existing v1 system.
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock

from trm_api.main import app


class TestV2APIIntegration:
    """Integration tests cho v2 API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_v2_health_endpoint(self, client):
        """Test v2 health check endpoint"""
        response = client.get("/v2/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"
        assert data["service"] == "TRM-OS Conversational Intelligence"
        assert "features" in data
        assert len(data["features"]) > 0
    
    def test_conversation_health_endpoint(self, client):
        """Test conversation health endpoint"""
        response = client.get("/v2/conversations/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "active_sessions" in data
        assert "websocket_connections" in data
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_create_session_endpoint(self, mock_get_user, client):
        """Test session creation endpoint"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        session_data = {
            "user_id": "test_user_123",
            "metadata": {"source": "web_app", "version": "v2.0"}
        }
        
        response = client.post(
            "/v2/conversations/sessions",
            json=session_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "session_id" in data
        assert data["user_id"] == "test_user_123"
        assert data["status"] == "active"
        assert "created_at" in data
        assert data["turn_count"] == 0
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_conversation_analysis_endpoint(self, mock_get_user, client):
        """Test conversation analysis endpoint"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        # First create a session
        session_data = {
            "user_id": "test_user_123",
            "metadata": {"source": "test"}
        }
        
        session_response = client.post(
            "/v2/conversations/sessions",
            json=session_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        session_id = session_response.json()["session_id"]
        
        # Now test conversation analysis
        conversation_data = {
            "message": "Tôi muốn tạo dự án Analytics Dashboard",
            "session_id": session_id,
            "language": "vi"
        }
        
        response = client.post(
            "/v2/conversations/analyze",
            json=conversation_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response_text" in data
        assert "intent_detected" in data
        assert "confidence" in data
        assert "session_id" in data
        assert "suggested_actions" in data
        assert "entities_extracted" in data
        assert "system_actions" in data
        assert "processing_time" in data
        
        # Verify intent detection
        assert data["intent_detected"] == "create_project"
        assert data["confidence"] > 0.5
        assert data["session_id"] == session_id
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_conversation_with_vietnamese_input(self, mock_get_user, client):
        """Test conversation với Vietnamese input"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        test_cases = [
            {
                "message": "Tôi cần trợ giúp từ data analyst agent",
                "expected_intent": "get_agent_help"
            },
            {
                "message": "Có vấn đề với hệ thống database",
                "expected_intent": "analyze_tension"
            },
            {
                "message": "Trạng thái dự án hiện tại thế nào?",
                "expected_intent": "check_status"
            }
        ]
        
        for test_case in test_cases:
            conversation_data = {
                "message": test_case["message"],
                "language": "vi"
            }
            
            response = client.post(
                "/v2/conversations/analyze",
                json=conversation_data,
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["intent_detected"] == test_case["expected_intent"]
            assert data["confidence"] > 0.5
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_conversation_with_english_input(self, mock_get_user, client):
        """Test conversation với English input"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        test_cases = [
            {
                "message": "I want to create a new project called DataPipeline",
                "expected_intent": "create_project"
            },
            {
                "message": "Need help from integration agent",
                "expected_intent": "get_agent_help"
            },
            {
                "message": "There's a performance problem with the API",
                "expected_intent": "analyze_tension"
            }
        ]
        
        for test_case in test_cases:
            conversation_data = {
                "message": test_case["message"],
                "language": "en"
            }
            
            response = client.post(
                "/v2/conversations/analyze",
                json=conversation_data,
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["intent_detected"] == test_case["expected_intent"]
            assert data["confidence"] > 0.5
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_session_management_workflow(self, mock_get_user, client):
        """Test complete session management workflow"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        # 1. Create session
        session_data = {
            "user_id": "test_user_123",
            "metadata": {"source": "integration_test"}
        }
        
        create_response = client.post(
            "/v2/conversations/sessions",
            json=session_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert create_response.status_code == 200
        session_id = create_response.json()["session_id"]
        
        # 2. Add conversation turns
        messages = [
            "Tôi muốn tạo dự án Analytics",
            "Cần data analyst agent cho dự án này",
            "Trạng thái dự án thế nào?"
        ]
        
        for message in messages:
            conversation_data = {
                "message": message,
                "session_id": session_id
            }
            
            response = client.post(
                "/v2/conversations/analyze",
                json=conversation_data,
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 200
        
        # 3. Get session info
        session_response = client.get(
            f"/v2/conversations/sessions/{session_id}",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert session_response.status_code == 200
        session_data = session_response.json()
        assert session_data["turn_count"] == 3
        
        # 4. Get conversation history
        history_response = client.get(
            f"/v2/conversations/sessions/{session_id}/history",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert history_response.status_code == 200
        history_data = history_response.json()
        assert history_data["turn_count"] == 3
        assert len(history_data["turns"]) == 3
        
        # 5. Get analytics
        analytics_response = client.get(
            f"/v2/conversations/sessions/{session_id}/analytics",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert analytics_response.status_code == 200
        analytics_data = analytics_response.json()
        assert analytics_data["turn_count"] == 3
        assert "intent_distribution" in analytics_data
        
        # 6. End session
        end_response = client.delete(
            f"/v2/conversations/sessions/{session_id}",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert end_response.status_code == 200
        
        # 7. Verify session is ended
        get_response = client.get(
            f"/v2/conversations/sessions/{session_id}",
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert get_response.status_code == 404
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_entity_extraction_and_system_actions(self, mock_get_user, client):
        """Test entity extraction và system action generation"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        conversation_data = {
            "message": "Tạo dự án E-commerce với data analyst agent, ưu tiên cao, deadline tuần này",
            "language": "vi"
        }
        
        response = client.post(
            "/v2/conversations/analyze",
            json=conversation_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check entity extraction
        entities = data["entities_extracted"]
        assert "project_name" in entities
        assert "agent_type" in entities
        assert "priority_level" in entities
        
        # Check system actions
        system_actions = data["system_actions"]
        assert len(system_actions) > 0
        
        main_action = system_actions[0]
        assert main_action["action_type"] == "create_entity"
        assert "parameters" in main_action
        assert main_action["confidence"] > 0.0
    
    def test_error_handling(self, client):
        """Test error handling cho invalid requests"""
        # Test without authentication
        response = client.post(
            "/v2/conversations/analyze",
            json={"message": "Test message"}
        )
        
        assert response.status_code == 401  # Unauthorized
        
        # Test invalid session ID
        with patch('trm_api.services.user_service.get_current_user') as mock_get_user:
            mock_user = MagicMock()
            mock_user.uid = "test_user_123"
            mock_user.username = "test_user"
            mock_get_user.return_value = mock_user
            
            response = client.get(
                "/v2/conversations/sessions/invalid_session_id",
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 404
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_performance_metrics(self, mock_get_user, client):
        """Test performance metrics trong responses"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        conversation_data = {
            "message": "Tôi muốn tạo dự án mới",
            "language": "vi"
        }
        
        response = client.post(
            "/v2/conversations/analyze",
            json=conversation_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check processing time is recorded
        assert "processing_time" in data
        assert data["processing_time"] >= 0  # Allow 0 for very fast test execution
        assert data["processing_time"] < 5.0  # Should be fast
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_contextual_suggestions(self, mock_get_user, client):
        """Test contextual suggestions generation"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        # Create session và add conversation turn
        session_data = {
            "user_id": "test_user_123",
            "metadata": {"source": "test"}
        }
        
        session_response = client.post(
            "/v2/conversations/sessions",
            json=session_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        session_id = session_response.json()["session_id"]
        
        # First turn: Create project
        conversation_data = {
            "message": "Tạo dự án Analytics Dashboard",
            "session_id": session_id
        }
        
        response = client.post(
            "/v2/conversations/analyze",
            json=conversation_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have suggested actions
        assert "suggested_actions" in data
        assert len(data["suggested_actions"]) > 0
        
        # Suggestions should be relevant to project creation
        suggestions = data["suggested_actions"]
        project_related = any("thành viên" in suggestion or "timeline" in suggestion or "task" in suggestion 
                            for suggestion in suggestions)
        assert project_related


class TestV2V1Integration:
    """Test integration between v2 conversational API và v1 system"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_v1_v2_coexistence(self, client):
        """Test v1 và v2 APIs coexist"""
        # Test v1 health
        v1_response = client.get("/health")
        assert v1_response.status_code == 200
        
        # Test v2 health
        v2_response = client.get("/v2/health")
        assert v2_response.status_code == 200
        
        # Both should work
        assert v1_response.json()["status"] == "ok"
        assert v2_response.json()["status"] == "healthy"
    
    @patch('trm_api.services.user_service.get_current_user')
    def test_v2_conversation_maps_to_v1_actions(self, mock_get_user, client):
        """Test v2 conversation analysis maps to v1 system actions"""
        mock_user = MagicMock()
        mock_user.uid = "test_user_123"
        mock_user.username = "test_user"
        mock_get_user.return_value = mock_user
        
        conversation_data = {
            "message": "Tôi muốn tạo dự án Analytics và cần data analyst agent",
            "language": "vi"
        }
        
        response = client.post(
            "/v2/conversations/analyze",
            json=conversation_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check system actions map to v1 endpoints
        system_actions = data["system_actions"]
        assert len(system_actions) > 0
        
        # Should map to v1 API endpoints
        v1_endpoints = [action["action_type"] for action in system_actions 
                      if any(endpoint in str(action) for endpoint in ["/api/v1/", "create_entity", "find_agent"])]
        assert len(v1_endpoints) > 0
    
    def test_openapi_documentation_includes_v2(self, client):
        """Test OpenAPI documentation includes v2 endpoints"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec.get("paths", {})
        
        # Should include v2 paths
        v2_paths = [path for path in paths.keys() if path.startswith("/v2/")]
        assert len(v2_paths) > 0
        
        # Should include conversation endpoints
        conversation_paths = [path for path in v2_paths if "conversation" in path]
        assert len(conversation_paths) > 0 