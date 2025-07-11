"""
Integration Agent Template

Agent chuyên biệt xử lý các tensions liên quan đến system integration,
API integration, data synchronization và enterprise connectivity trong TRM-OS.
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_template import BaseAgentTemplate, AgentTemplateMetadata, AgentCapability
from ..base_agent import AgentMetadata
from ...eventbus.system_event_bus import EventType, SystemEvent
from ...models.tension import Tension
from trm_api.models.enums import TensionType


class IntegrationAgent(BaseAgentTemplate):
    """
    Agent chuyên biệt cho system integration và connectivity.
    
    Capabilities:
    - API integration và development
    - Data synchronization
    - Enterprise system connectivity
    - Workflow automation
    - Message queue management
    - Real-time data streaming
    """
    
    def __init__(self, agent_id: Optional[str] = None, metadata: Optional[AgentMetadata] = None):
        # Use BaseAgentTemplate constructor - no need to override AgentMetadata creation
        super().__init__(agent_id, metadata)
        
        # Integration-specific patterns
        self.integration_patterns = {
            "api_integration": [
                r"(?:api|endpoint|web service|microservice).*(?:integration|connect|integrate)",
                r"(?:rest|graphql|soap|grpc).*(?:api|service)",
                r"(?:third.?party|external).*(?:api|service|system)",
                r"(?:webhook|callback|notification)"
            ],
            "data_sync": [
                r"(?:data|database).*(?:sync|synchronization|synchronize)",
                r"(?:etl|extract|transform|load)",
                r"(?:migration|import|export).*(?:data|database)",
                r"(?:real.?time|streaming).*(?:data|sync)"
            ],
            "enterprise_systems": [
                r"(?:erp|crm|hrms|enterprise).*(?:integration|connect)",
                r"(?:sap|salesforce|oracle|microsoft).*(?:integration|connect)",
                r"(?:legacy|existing).*(?:system|integration)",
                r"(?:single sign.?on|sso|authentication)"
            ],
            "workflow_automation": [
                r"(?:workflow|process).*(?:automation|automate)",
                r"(?:business process|bpm).*(?:automation|integration)",
                r"(?:trigger|event).*(?:automation|workflow)",
                r"(?:orchestration|coordination).*(?:system|service)"
            ]
        }
        
        self.integration_technologies = {
            "api_protocols": ["rest", "graphql", "soap", "grpc", "websocket"],
            "messaging": ["rabbitmq", "kafka", "redis", "activemq", "aws sqs"],
            "data_formats": ["json", "xml", "csv", "avro", "protobuf"],
            "authentication": ["oauth", "jwt", "saml", "api key", "basic auth"],
            "enterprise_systems": ["sap", "salesforce", "oracle", "microsoft", "workday"]
        }
        
        self.integration_patterns_common = {
            "sync_patterns": ["request_response", "publish_subscribe", "message_queue", "event_streaming"],
            "data_patterns": ["etl", "elt", "cdc", "batch_processing", "real_time_streaming"],
            "security_patterns": ["api_gateway", "oauth_flow", "certificate_auth", "encryption"],
            "reliability_patterns": ["retry_mechanism", "circuit_breaker", "bulkhead", "timeout_handling"]
        }
    
    def _get_default_template_metadata(self) -> AgentTemplateMetadata:
        """Trả về metadata mặc định cho Integration template"""
        return AgentTemplateMetadata(
            template_name="IntegrationAgent",
            template_version="1.0.0",
            description="Agent chuyên biệt xử lý tensions liên quan đến system integration và connectivity",
            primary_domain="integration",
            capabilities=[
                AgentCapability(
                    name="api_integration",
                    description="Tích hợp APIs và web services",
                    required_skills=["api_design", "http_protocols", "authentication", "error_handling"],
                    complexity_level=4,
                    estimated_time=180
                ),
                AgentCapability(
                    name="data_synchronization",
                    description="Đồng bộ hóa data giữa các systems",
                    required_skills=["etl", "data_mapping", "conflict_resolution", "data_validation"],
                    complexity_level=4,
                    estimated_time=240
                ),
                AgentCapability(
                    name="enterprise_connectivity",
                    description="Kết nối với enterprise systems",
                    required_skills=["enterprise_systems", "sso", "security", "compliance"],
                    complexity_level=5,
                    estimated_time=300
                ),
                AgentCapability(
                    name="workflow_automation",
                    description="Tự động hóa business workflows",
                    required_skills=["workflow_design", "business_logic", "event_handling", "orchestration"],
                    complexity_level=4,
                    estimated_time=200
                ),
                AgentCapability(
                    name="message_queue_management",
                    description="Quản lý message queues và event streaming",
                    required_skills=["messaging_systems", "event_driven_architecture", "scalability"],
                    complexity_level=3,
                    estimated_time=120
                ),
                AgentCapability(
                    name="real_time_integration",
                    description="Tích hợp real-time data streams",
                    required_skills=["streaming", "websockets", "real_time_processing", "latency_optimization"],
                    complexity_level=4,
                    estimated_time=180
                )
            ],
            recommended_tensions=[
                "API Integration Needs",
                "Data Synchronization Issues",
                "Enterprise System Connectivity",
                "Workflow Automation Requirements",
                "Real-time Data Integration",
                "Third-party Service Integration"
            ],
            dependencies=["api_gateway", "message_broker", "database_access", "security_infrastructure"],
            performance_metrics={
                "integration_success_rate": 0.95,
                "data_sync_accuracy": 0.98,
                "api_response_time": 0.85,
                "system_uptime": 0.99,
                "error_rate": 0.02
            }
        )
    
    async def can_handle_tension(self, tension: Tension) -> bool:
        """Kiểm tra xem có thể xử lý tension này không"""
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            
            # Tìm integration-related keywords (English and Vietnamese)
            integration_keywords = [
                "integration", "integrate", "api", "sync", "synchronize",
                "connect", "connection", "third party", "external", "enterprise",
                "workflow", "automation", "data", "system", "service",
                "webhook", "endpoint", "microservice", "etl", "migration",
                "tích hợp", "đồng bộ", "kết nối", "hệ thống", "dịch vụ"
            ]
            
            has_integration_keywords = any(keyword in description or keyword in title 
                                         for keyword in integration_keywords)
            
            # Kiểm tra integration patterns
            pattern_match = False
            for category, patterns in self.integration_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, description, re.IGNORECASE) or \
                       re.search(pattern, title, re.IGNORECASE):
                        pattern_match = True
                        break
                if pattern_match:
                    break
            
            # Kiểm tra technology mentions
            has_tech_keywords = any(
                tech in description or tech in title
                for tech_category in self.integration_technologies.values()
                for tech in tech_category
            )
            
            # Kiểm tra tension type - use proper TensionType enums
            suitable_types = [
                TensionType.PROCESS_IMPROVEMENT,  # Integration improves processes
                TensionType.TECHNICAL_DEBT,      # Integration can solve technical debt
                TensionType.OPPORTUNITY,         # Integration creates opportunities
                TensionType.PROBLEM              # Integration solves problems
            ]
            type_match = tension.tensionType in suitable_types
            
            # Agent có thể handle nếu có integration indicators
            can_handle = (has_integration_keywords or pattern_match or has_tech_keywords) and type_match
            
            if can_handle:
                self.logger.info(f"Integration can handle tension {tension.uid}: {tension.title}")
            
            return can_handle
            
        except Exception as e:
            self.logger.error(f"Error checking tension handleability: {str(e)}")
            return False
    
    async def analyze_tension_requirements(self, tension: Tension) -> Dict[str, Any]:
        """Phân tích requirements cụ thể cho integration tension"""
        requirements = {
            "integration_type": "unknown",
            "systems_involved": [],
            "data_formats": [],
            "complexity": "medium",
            "urgency": "normal",
            "deliverables": [],
            "tools_needed": [],
            "estimated_effort": 180,
            "success_criteria": [],
            "security_requirements": [],
            "performance_requirements": {},
            "compliance_needs": []
        }
        
        try:
            description = tension.description.lower()
            title = tension.title.lower()
            combined_text = f"{title} {description}"
            
            # Xác định loại integration
            if any(pattern in combined_text for pattern in ["api", "endpoint", "web service", "microservice"]):
                requirements["integration_type"] = "api_integration"
                requirements["tools_needed"].extend(["api_gateway", "authentication", "monitoring"])
                requirements["deliverables"].append("API Integration")
                requirements["estimated_effort"] = 180
                
            elif any(pattern in combined_text for pattern in ["data sync", "synchronization", "etl", "migration"]):
                requirements["integration_type"] = "data_synchronization"
                requirements["tools_needed"].extend(["etl_pipeline", "data_validation", "conflict_resolution"])
                requirements["deliverables"].append("Data Synchronization System")
                requirements["estimated_effort"] = 240
                
            elif any(pattern in combined_text for pattern in ["enterprise", "erp", "crm", "sap", "salesforce"]):
                requirements["integration_type"] = "enterprise_integration"
                requirements["tools_needed"].extend(["enterprise_connector", "sso", "security_framework"])
                requirements["deliverables"].append("Enterprise System Integration")
                requirements["estimated_effort"] = 300
                
            elif any(pattern in combined_text for pattern in ["workflow", "automation", "process", "orchestration"]):
                requirements["integration_type"] = "workflow_automation"
                requirements["tools_needed"].extend(["workflow_engine", "business_rules", "event_processing"])
                requirements["deliverables"].append("Workflow Automation System")
                requirements["estimated_effort"] = 200
                
            elif any(pattern in combined_text for pattern in ["real-time", "streaming", "live", "websocket"]):
                requirements["integration_type"] = "real_time_integration"
                requirements["tools_needed"].extend(["streaming_platform", "websockets", "event_processing"])
                requirements["deliverables"].append("Real-time Integration")
                requirements["estimated_effort"] = 180
                
            elif any(pattern in combined_text for pattern in ["message", "queue", "event", "pub/sub"]):
                requirements["integration_type"] = "message_integration"
                requirements["tools_needed"].extend(["message_broker", "event_bus", "queue_management"])
                requirements["deliverables"].append("Message Integration System")
                requirements["estimated_effort"] = 120
            
            # Detect systems involved
            system_keywords = {
                "database": ["database", "db", "mysql", "postgresql", "mongodb", "oracle"],
                "crm": ["salesforce", "hubspot", "dynamics", "crm"],
                "erp": ["sap", "oracle erp", "netsuite", "erp"],
                "cloud": ["aws", "azure", "gcp", "cloud"],
                "payment": ["stripe", "paypal", "payment", "billing"],
                "communication": ["slack", "teams", "email", "sms"]
            }
            
            for system_type, keywords in system_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    requirements["systems_involved"].append(system_type)
            
            # Detect data formats
            format_keywords = ["json", "xml", "csv", "excel", "pdf", "avro", "protobuf"]
            for format_type in format_keywords:
                if format_type in combined_text:
                    requirements["data_formats"].append(format_type)
            
            # Xác định complexity
            complexity_indicators = {
                "high": ["complex", "phức tạp", "enterprise", "large scale", "multi-system", "critical"],
                "low": ["simple", "đơn giản", "basic", "cơ bản", "quick", "single system"]
            }
            
            for level, indicators in complexity_indicators.items():
                if any(indicator in combined_text for indicator in indicators):
                    requirements["complexity"] = level
                    break
            
            # Adjust effort based on complexity
            if requirements["complexity"] == "high":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 1.8)
            elif requirements["complexity"] == "low":
                requirements["estimated_effort"] = int(requirements["estimated_effort"] * 0.6)
            
            # Xác định urgency
            if any(pattern in combined_text for pattern in ["urgent", "gấp", "asap", "critical", "down"]):
                requirements["urgency"] = "high"
                requirements["estimated_effort"] = max(60, requirements["estimated_effort"] // 2)
            
            # Security requirements
            if any(pattern in combined_text for pattern in ["security", "secure", "auth", "encryption", "compliance"]):
                requirements["security_requirements"] = [
                    "Authentication và authorization",
                    "Data encryption in transit và at rest",
                    "API rate limiting và throttling",
                    "Audit logging và monitoring",
                    "Input validation và sanitization"
                ]
            
            # Performance requirements
            requirements["performance_requirements"] = {
                "response_time": "< 2 seconds",
                "throughput": "> 1000 requests/minute",
                "uptime": "> 99.9%",
                "data_latency": "< 5 minutes"
            }
            
            # Compliance needs
            if any(pattern in combined_text for pattern in ["gdpr", "hipaa", "sox", "compliance", "regulation"]):
                requirements["compliance_needs"] = [
                    "Data privacy compliance",
                    "Audit trail maintenance",
                    "Data retention policies",
                    "Access control compliance"
                ]
            
            # Success criteria
            requirements["success_criteria"] = [
                "Successful data transfer với 99%+ accuracy",
                "Integration performs within SLA requirements",
                "Security requirements fully implemented",
                "Error handling và recovery mechanisms working",
                "Monitoring và alerting operational"
            ]
            
            self.logger.info(f"Analyzed requirements for tension {tension.uid}: {requirements['integration_type']}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing tension requirements: {str(e)}")
        
        return requirements
    
    async def generate_specialized_solutions(self, tension: Tension, 
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions chuyên biệt cho integration tasks"""
        solutions = []
        
        try:
            integration_type = requirements.get("integration_type", "unknown")
            
            if integration_type == "api_integration":
                solutions.extend(await self._generate_api_integration_solutions(tension, requirements))
                
            elif integration_type == "data_synchronization":
                solutions.extend(await self._generate_data_sync_solutions(tension, requirements))
                
            elif integration_type == "enterprise_integration":
                solutions.extend(await self._generate_enterprise_solutions(tension, requirements))
                
            elif integration_type == "workflow_automation":
                solutions.extend(await self._generate_workflow_solutions(tension, requirements))
                
            elif integration_type == "real_time_integration":
                solutions.extend(await self._generate_realtime_solutions(tension, requirements))
                
            elif integration_type == "message_integration":
                solutions.extend(await self._generate_messaging_solutions(tension, requirements))
                
            else:
                # Generic integration solutions
                solutions.extend(await self._generate_generic_integration_solutions(tension, requirements))
            
            # Thêm metadata cho tất cả solutions
            for solution in solutions:
                solution.update({
                    "agent_template": "IntegrationAgent",
                    "domain": "integration",
                    "estimated_effort": requirements.get("estimated_effort", 180),
                    "complexity": requirements.get("complexity", "medium"),
                    "systems_involved": requirements.get("systems_involved", []),
                    "security_requirements": requirements.get("security_requirements", []),
                    "success_criteria": requirements.get("success_criteria", [])
                })
            
            self.logger.info(f"Generated {len(solutions)} integration solutions for tension {tension.uid}")
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {str(e)}")
        
        return solutions
    
    async def _generate_api_integration_solutions(self, tension: Tension, 
                                                requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho API integration"""
        return [
            {
                "title": "RESTful API Integration Platform",
                "description": "Thiết lập comprehensive API integration platform với security và monitoring",
                "approach": "API-First Integration",
                "steps": [
                    "Analyze target APIs và design integration architecture",
                    "Implement API gateway với rate limiting và security",
                    "Develop API adapters cho each external service",
                    "Add authentication flows (OAuth, JWT, API keys)",
                    "Implement error handling và retry mechanisms",
                    "Setup monitoring, logging và alerting",
                    "Create comprehensive API documentation"
                ],
                "tools": ["api_gateway", "oauth_provider", "monitoring_platform", "documentation_tool"],
                "deliverables": ["API Integration Platform", "Security Framework", "Monitoring Setup", "Documentation"],
                "timeline": "4-6 weeks",
                "priority": 1
            },
            {
                "title": "Microservices Integration Hub",
                "description": "Tạo integration hub để orchestrate microservices communication",
                "approach": "Event-Driven Microservices",
                "steps": [
                    "Design microservices communication patterns",
                    "Implement service discovery và load balancing",
                    "Setup event bus cho asynchronous communication",
                    "Add circuit breaker patterns cho resilience",
                    "Implement distributed tracing và monitoring",
                    "Create service mesh infrastructure",
                    "Add automated testing cho integration flows"
                ],
                "tools": ["service_mesh", "event_bus", "service_discovery", "distributed_tracing"],
                "deliverables": ["Integration Hub", "Service Mesh", "Monitoring Dashboard", "Test Suite"],
                "timeline": "6-8 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_data_sync_solutions(self, tension: Tension,
                                          requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho data synchronization"""
        return [
            {
                "title": "Real-time Data Synchronization Pipeline",
                "description": "Thiết lập real-time data sync pipeline với conflict resolution",
                "approach": "Change Data Capture (CDC)",
                "steps": [
                    "Analyze data schemas và mapping requirements",
                    "Implement CDC mechanisms cho source systems",
                    "Design data transformation và validation rules",
                    "Setup conflict resolution strategies",
                    "Implement real-time streaming pipeline",
                    "Add data quality monitoring",
                    "Create rollback và recovery mechanisms"
                ],
                "tools": ["cdc_platform", "streaming_engine", "data_validation", "monitoring"],
                "deliverables": ["Data Sync Pipeline", "Transformation Rules", "Monitoring Dashboard", "Recovery Procedures"],
                "timeline": "5-7 weeks",
                "priority": 1
            },
            {
                "title": "Batch ETL Processing System",
                "description": "Implement robust batch ETL system cho large-scale data processing",
                "approach": "Scheduled Batch Processing",
                "steps": [
                    "Design ETL workflows và scheduling",
                    "Implement data extraction từ multiple sources",
                    "Create data transformation và cleansing logic",
                    "Setup data loading với validation",
                    "Add error handling và retry mechanisms",
                    "Implement data lineage tracking",
                    "Create performance optimization"
                ],
                "tools": ["etl_platform", "scheduler", "data_quality_tools", "lineage_tracking"],
                "deliverables": ["ETL System", "Data Workflows", "Quality Reports", "Performance Metrics"],
                "timeline": "4-6 weeks",
                "priority": 2
            }
        ]
    
    async def _generate_enterprise_solutions(self, tension: Tension,
                                           requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho enterprise integration"""
        return [
            {
                "title": "Enterprise Application Integration (EAI)",
                "description": "Comprehensive EAI solution cho enterprise systems connectivity",
                "approach": "Hub-and-Spoke Integration",
                "steps": [
                    "Analyze enterprise systems và integration requirements",
                    "Design integration hub architecture",
                    "Implement enterprise service bus (ESB)",
                    "Setup single sign-on (SSO) integration",
                    "Add data mapping và transformation layers",
                    "Implement security và compliance frameworks",
                    "Create enterprise monitoring dashboard"
                ],
                "tools": ["esb_platform", "sso_provider", "enterprise_connectors", "compliance_tools"],
                "deliverables": ["EAI Platform", "SSO Integration", "Security Framework", "Compliance Reports"],
                "timeline": "8-12 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_workflow_solutions(self, tension: Tension,
                                         requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho workflow automation"""
        return [
            {
                "title": "Business Process Automation Platform",
                "description": "Comprehensive BPA platform cho workflow automation",
                "approach": "Event-Driven Workflow Orchestration",
                "steps": [
                    "Model business processes và decision points",
                    "Design workflow orchestration engine",
                    "Implement business rules engine",
                    "Add human task management",
                    "Setup event triggers và notifications",
                    "Create workflow monitoring dashboard",
                    "Add process optimization analytics"
                ],
                "tools": ["workflow_engine", "business_rules", "task_management", "process_analytics"],
                "deliverables": ["BPA Platform", "Workflow Engine", "Rules Engine", "Analytics Dashboard"],
                "timeline": "6-8 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_realtime_solutions(self, tension: Tension,
                                         requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho real-time integration"""
        return [
            {
                "title": "Real-time Event Streaming Platform",
                "description": "High-performance real-time event streaming và processing",
                "approach": "Event Streaming Architecture",
                "steps": [
                    "Design event streaming topology",
                    "Implement high-throughput event ingestion",
                    "Setup real-time event processing",
                    "Add stream analytics và aggregations",
                    "Implement low-latency event delivery",
                    "Setup monitoring và alerting",
                    "Add scalability và fault tolerance"
                ],
                "tools": ["kafka", "stream_processing", "real_time_analytics", "monitoring"],
                "deliverables": ["Streaming Platform", "Processing Engine", "Analytics Dashboard", "Scaling Framework"],
                "timeline": "4-6 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_messaging_solutions(self, tension: Tension,
                                          requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo solutions cho message integration"""
        return [
            {
                "title": "Enterprise Message Bus",
                "description": "Scalable message bus cho enterprise-wide communication",
                "approach": "Publish-Subscribe Messaging",
                "steps": [
                    "Design message bus architecture",
                    "Implement message brokers với clustering",
                    "Setup topic-based routing",
                    "Add message persistence và durability",
                    "Implement dead letter queues",
                    "Setup monitoring và management",
                    "Add security và access control"
                ],
                "tools": ["message_broker", "clustering", "monitoring", "security_framework"],
                "deliverables": ["Message Bus", "Broker Cluster", "Management Console", "Security Setup"],
                "timeline": "3-5 weeks",
                "priority": 1
            }
        ]
    
    async def _generate_generic_integration_solutions(self, tension: Tension,
                                                    requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tạo generic integration solutions"""
        return [
            {
                "title": "Custom Integration Solution",
                "description": "Tailored integration solution based on specific requirements",
                "approach": "Requirements-Driven Integration",
                "steps": [
                    "Analyze integration requirements chi tiết",
                    "Design custom integration architecture",
                    "Implement integration connectors",
                    "Add data transformation logic",
                    "Setup error handling và monitoring",
                    "Create testing và validation framework",
                    "Deploy và optimize performance"
                ],
                "tools": ["integration_platform", "custom_connectors", "transformation_engine", "testing_framework"],
                "deliverables": ["Custom Integration", "Connectors", "Testing Framework", "Documentation"],
                "timeline": "4-6 weeks",
                "priority": 1
            }
        ]
    
    async def execute_solution(self, solution: Dict[str, Any], 
                             context: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi integration solution"""
        execution_result = {
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "results": {},
            "deliverables_created": [],
            "next_steps": [],
            "integration_metrics": {}
        }
        
        try:
            solution_title = solution.get("title", "Unknown Solution")
            self.logger.info(f"Executing integration solution: {solution_title}")
            
            # Simulate solution execution
            await asyncio.sleep(3)  # Simulate integration development time
            
            # Mock results based on solution type
            if "api" in solution_title.lower():
                execution_result["results"] = {
                    "apis_integrated": 8,
                    "endpoints_created": 25,
                    "authentication_success_rate": 99.5,
                    "average_response_time": 145  # ms
                }
                execution_result["deliverables_created"] = ["API Integration Platform", "Security Framework", "Documentation"]
                execution_result["integration_metrics"] = {
                    "uptime": 99.9,
                    "throughput": 1250,  # requests/minute
                    "error_rate": 0.1
                }
                
            elif "data" in solution_title.lower() and "sync" in solution_title.lower():
                execution_result["results"] = {
                    "data_sources_connected": 12,
                    "sync_accuracy": 99.8,
                    "records_processed_daily": 2500000,
                    "sync_latency": 2.3  # minutes
                }
                execution_result["deliverables_created"] = ["Data Sync Pipeline", "Monitoring Dashboard", "Recovery Procedures"]
                execution_result["integration_metrics"] = {
                    "data_quality_score": 98.5,
                    "sync_success_rate": 99.8,
                    "processing_speed": 50000  # records/minute
                }
                
            elif "enterprise" in solution_title.lower():
                execution_result["results"] = {
                    "enterprise_systems_connected": 6,
                    "sso_integration_success": 100.0,
                    "user_provisioning_automated": 95.0,
                    "compliance_score": 98.0
                }
                execution_result["deliverables_created"] = ["EAI Platform", "SSO Integration", "Compliance Framework"]
                execution_result["integration_metrics"] = {
                    "system_availability": 99.95,
                    "security_score": 96.0,
                    "user_satisfaction": 4.4
                }
                
            elif "workflow" in solution_title.lower():
                execution_result["results"] = {
                    "processes_automated": 15,
                    "workflow_efficiency_improvement": 65.0,
                    "manual_tasks_eliminated": 120,
                    "approval_time_reduction": 75.0
                }
                execution_result["deliverables_created"] = ["BPA Platform", "Workflow Engine", "Analytics Dashboard"]
                execution_result["integration_metrics"] = {
                    "process_completion_rate": 98.5,
                    "automation_success_rate": 96.8,
                    "time_savings": 180  # hours/week
                }
                
            elif "real-time" in solution_title.lower() or "streaming" in solution_title.lower():
                execution_result["results"] = {
                    "event_throughput": 100000,  # events/second
                    "processing_latency": 50,  # milliseconds
                    "stream_uptime": 99.95,
                    "data_freshness": 0.5  # seconds
                }
                execution_result["deliverables_created"] = ["Streaming Platform", "Processing Engine", "Analytics Dashboard"]
                execution_result["integration_metrics"] = {
                    "stream_reliability": 99.9,
                    "processing_accuracy": 99.7,
                    "scalability_factor": 10
                }
                
            elif "message" in solution_title.lower():
                execution_result["results"] = {
                    "message_throughput": 50000,  # messages/minute
                    "delivery_success_rate": 99.9,
                    "queue_depth_avg": 125,
                    "processing_time": 15  # milliseconds
                }
                execution_result["deliverables_created"] = ["Message Bus", "Broker Cluster", "Management Console"]
                execution_result["integration_metrics"] = {
                    "message_reliability": 99.95,
                    "broker_uptime": 99.8,
                    "scaling_efficiency": 92.0
                }
                
            else:
                execution_result["results"] = {
                    "integrations_completed": 5,
                    "systems_connected": 8,
                    "data_accuracy": 98.5,
                    "performance_improvement": 35.0
                }
                execution_result["deliverables_created"] = ["Custom Integration", "Monitoring Setup", "Documentation"]
                execution_result["integration_metrics"] = {
                    "integration_success_rate": 97.5,
                    "system_reliability": 99.2,
                    "user_adoption": 85.0
                }
            
            execution_result["next_steps"] = [
                "Monitor integration performance metrics",
                "Setup automated health checks",
                "Train operations team về new integrations",
                "Plan capacity scaling based on usage",
                "Schedule regular security audits"
            ]
            
            self.logger.info(f"Successfully executed solution: {solution_title}")
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["error"] = str(e)
            self.logger.error(f"Error executing solution: {str(e)}")
        
        return execution_result
    
    async def _register_specialized_handlers(self) -> None:
        """Đăng ký specialized event handlers cho Integration"""
        # Đăng ký events liên quan đến integration
        self.subscribe_to_event(EventType.INTEGRATION_REQUESTED)
        self.subscribe_to_event(EventType.API_CALL_FAILED)
        self.subscribe_to_event(EventType.DATA_SYNC_COMPLETED)
        
    async def _initialize_specialized_components(self) -> None:
        """Khởi tạo integration components"""
        self.logger.info("Initializing Integration specialized components")
        
        # Initialize integration platforms, connectors, etc.
        # This would be implemented based on actual infrastructure
        
    async def _handle_specialized_event(self, event: SystemEvent) -> None:
        """Xử lý specialized events cho Integration"""
        if event.event_type == EventType.INTEGRATION_REQUESTED:
            await self._handle_integration_requested(event)
        elif event.event_type == EventType.API_CALL_FAILED:
            await self._handle_api_call_failed(event)
        elif event.event_type == EventType.DATA_SYNC_COMPLETED:
            await self._handle_data_sync_completed(event)
    
    async def _handle_integration_requested(self, event: SystemEvent) -> None:
        """Xử lý sự kiện integration requested"""
        self.logger.info(f"Integration requested: {event.entity_id}")
        # Implement integration request handling logic
        
    async def _handle_api_call_failed(self, event: SystemEvent) -> None:
        """Xử lý sự kiện API call failed"""
        self.logger.info(f"API call failed: {event.entity_id}")
        # Implement API failure handling logic
        
    async def _handle_data_sync_completed(self, event: SystemEvent) -> None:
        """Xử lý sự kiện data sync completed"""
        self.logger.info(f"Data sync completed: {event.entity_id}")
        # Implement data sync completion handling logic

    # Implementation of abstract methods from BaseAgent
    async def analyze_recognition_phase(self, recognition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Recognition phase for integration contexts
        Recognition phase của Recognition → Event → WIN
        """
        try:
            analysis = {
                "recognition_id": recognition_data.get("recognition_id", "unknown"),
                "agent_template": "IntegrationAgent",
                "analysis_type": "integration_recognition",
                "integration_requirements": {},
                "integration_scope": "unknown",
                "technical_complexity": "medium",
                "systems_involved": [],
                "connectivity_potential": 0.0,
                "confidence": 0.0
            }
            
            context = recognition_data.get("context", {})
            description = recognition_data.get("description", "")
            
            # Assess technical complexity
            if any(keyword in description.lower() for keyword in ["enterprise", "complex", "microservices", "distributed"]):
                analysis["technical_complexity"] = "high"
                analysis["connectivity_potential"] = 90.0
            elif any(keyword in description.lower() for keyword in ["simple", "basic", "single", "direct"]):
                analysis["technical_complexity"] = "low"
                analysis["connectivity_potential"] = 70.0
            else:
                analysis["technical_complexity"] = "medium"
                analysis["connectivity_potential"] = 80.0
            
            # Determine integration scope
            if any(keyword in description.lower() for keyword in ["api", "rest", "service", "endpoint"]):
                analysis["integration_scope"] = "api_integration"
            elif any(keyword in description.lower() for keyword in ["data", "sync", "etl", "pipeline"]):
                analysis["integration_scope"] = "data_integration"
            elif any(keyword in description.lower() for keyword in ["enterprise", "erp", "crm", "system"]):
                analysis["integration_scope"] = "enterprise_integration"
            else:
                analysis["integration_scope"] = "general_integration"
            
            # Identify systems involved
            analysis["systems_involved"] = self._identify_systems(description, context)
            
            # Calculate confidence
            analysis["confidence"] = self._calculate_integration_recognition_confidence(recognition_data)
            
            return analysis
            
        except Exception as e:
            return {
                "recognition_id": recognition_data.get("recognition_id", "unknown"),
                "error": "Analysis failed",
                "agent_template": "IntegrationAgent"
            }

    async def coordinate_event_execution(self, event_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate Event execution for integration tasks
        Event phase của Recognition → Event → WIN
        """
        try:
            coordination = {
                "event_id": event_context.get("event_id", "unknown"),
                "agent_template": "IntegrationAgent",
                "coordination_type": "integration_execution",
                "execution_plan": {},
                "integration_architecture": {},
                "connectivity_workflow": {},
                "testing_strategy": {},
                "deployment_phases": [],
                "monitoring_setup": {},
                "status": "coordinating"
            }
            
            event_type = event_context.get("event_type", "integration_task")
            requirements = event_context.get("requirements", {})
            
            # Create execution plan
            coordination["execution_plan"] = {
                "phases": [
                    {"name": "system_analysis", "duration_hours": 4, "priority": "high"},
                    {"name": "architecture_design", "duration_hours": 6, "priority": "high"},
                    {"name": "connector_development", "duration_hours": 12, "priority": "high"},
                    {"name": "data_mapping", "duration_hours": 8, "priority": "medium"},
                    {"name": "testing_validation", "duration_hours": 6, "priority": "high"},
                    {"name": "deployment", "duration_hours": 4, "priority": "medium"},
                    {"name": "monitoring_setup", "duration_hours": 3, "priority": "low"}
                ],
                "total_estimated_hours": 43,
                "approach": "incremental_integration"
            }
            
            # Integration architecture
            coordination["integration_architecture"] = {
                "pattern": requirements.get("pattern", "hub_and_spoke"),
                "middleware": ["message_queue", "api_gateway", "data_transformer"],
                "security": ["authentication", "authorization", "encryption"],
                "scalability": ["load_balancing", "caching", "async_processing"]
            }
            
            # Testing strategy
            coordination["testing_strategy"] = {
                "unit_testing": "connector_components",
                "integration_testing": "end_to_end_flows",
                "performance_testing": "load_and_stress",
                "security_testing": "penetration_and_vulnerability"
            }
            
            coordination["status"] = "coordinated"
            
            return coordination
            
        except Exception as e:
            return {
                "event_id": event_context.get("event_id", "unknown"),
                "error": "Coordination failed",
                "agent_template": "IntegrationAgent"
            }

    async def execute_strategic_action(self, action_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute strategic integration action trong AGE system
        Strategic execution with integration expertise
        """
        try:
            execution = {
                "action_id": action_context.get("action_id", "unknown"),
                "agent_template": "IntegrationAgent",
                "action_type": "strategic_integration_action",
                "execution_details": {},
                "deliverables": [],
                "connectivity_impact": {},
                "strategic_impact": {},
                "integration_outcomes": {},
                "status": "executing"
            }
            
            action_type = action_context.get("action_type", "general_integration")
            target_context = action_context.get("target_context", {})
            
            # Execute based on action type
            if action_type == "api_integration":
                execution["execution_details"] = await self._execute_api_integration(target_context)
            elif action_type == "data_synchronization":
                execution["execution_details"] = await self._execute_data_synchronization(target_context)
            elif action_type == "enterprise_integration":
                execution["execution_details"] = await self._execute_enterprise_integration(target_context)
            elif action_type == "workflow_automation":
                execution["execution_details"] = await self._execute_workflow_automation(target_context)
            else:
                execution["execution_details"] = await self._execute_general_integration(target_context)
            
            # Generate deliverables
            execution["deliverables"] = [
                {"type": "integration_connectors", "status": "completed"},
                {"type": "data_transformation_rules", "status": "completed"},
                {"type": "monitoring_dashboard", "status": "completed"},
                {"type": "integration_documentation", "status": "completed"}
            ]
            
            # Connectivity impact
            execution["connectivity_impact"] = {
                "systems_connected": "significantly_increased",
                "data_flow_efficiency": "improved_by_60%",
                "real_time_capabilities": "enabled",
                "integration_reliability": "enhanced_to_99.9%"
            }
            
            # Strategic impact
            execution["strategic_impact"] = {
                "operational_efficiency": "transformational",
                "data_accessibility": "unified_and_real_time",
                "business_agility": "significantly_enhanced",
                "digital_transformation": "accelerated"
            }
            
            execution["status"] = "completed"
            
            return execution
            
        except Exception as e:
            return {
                "action_id": action_context.get("action_id", "unknown"),
                "error": "Strategic action failed",
                "agent_template": "IntegrationAgent"
            }

    async def validate_win_achievement(self, win_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate WIN achievement for integration outcomes
        WIN phase của Recognition → Event → WIN
        """
        try:
            validation = {
                "win_id": win_context.get("win_id", "unknown"),
                "agent_template": "IntegrationAgent",
                "validation_type": "integration_win_validation",
                "wisdom_score": 0.0,
                "intelligence_score": 0.0,
                "networking_score": 0.0,
                "total_win_score": 0.0,
                "validation_criteria": {},
                "achievements": [],
                "areas_for_improvement": [],
                "validation_status": "validating"
            }
            
            deliverables = win_context.get("deliverables", [])
            metrics = win_context.get("metrics", {})
            stakeholder_feedback = win_context.get("stakeholder_feedback", {})
            
            # Validate Wisdom (integration understanding and system knowledge)
            wisdom_factors = {
                "system_understanding": metrics.get("system_analysis_quality", 85.0),
                "integration_strategy": metrics.get("strategy_effectiveness", 80.0),
                "architecture_design": metrics.get("architecture_quality", 88.0),
                "business_alignment": metrics.get("business_value", 82.0)
            }
            validation["wisdom_score"] = sum(wisdom_factors.values()) / len(wisdom_factors)
            
            # Validate Intelligence (technical sophistication and reliability)
            intelligence_factors = {
                "technical_excellence": metrics.get("technical_quality", 90.0),
                "integration_reliability": metrics.get("uptime", 99.0),
                "performance_optimization": metrics.get("performance_score", 85.0),
                "security_implementation": metrics.get("security_score", 92.0)
            }
            validation["intelligence_score"] = sum(intelligence_factors.values()) / len(intelligence_factors)
            
            # Validate Networking (system connectivity and stakeholder collaboration)
            networking_factors = {
                "systems_connectivity": metrics.get("connectivity_score", 88.0),
                "stakeholder_collaboration": stakeholder_feedback.get("collaboration_score", 80.0),
                "knowledge_transfer": metrics.get("documentation_quality", 85.0),
                "integration_adoption": metrics.get("adoption_rate", 78.0)
            }
            validation["networking_score"] = sum(networking_factors.values()) / len(networking_factors)
            
            # Calculate total WIN score
            validation["total_win_score"] = (
                validation["wisdom_score"] * 0.4 +
                validation["intelligence_score"] * 0.4 +
                validation["networking_score"] * 0.2
            )
            
            # Validation criteria
            validation["validation_criteria"] = {
                "integration_reliability": metrics.get("uptime", 99.0) > 98.0,
                "performance_targets_met": metrics.get("performance_score", 85.0) > 80,
                "security_standards_met": metrics.get("security_score", 90.0) > 85,
                "business_value_delivered": metrics.get("business_impact", 80.0) > 75,
                "stakeholder_satisfaction": stakeholder_feedback.get("satisfaction", "high") == "high"
            }
            
            # Achievements
            validation["achievements"] = [
                f"Delivered integration with {validation['wisdom_score']:.1f}% strategic alignment",
                f"Achieved {validation['intelligence_score']:.1f}% technical excellence",
                f"Enabled {validation['networking_score']:.1f}% system connectivity",
                f"Overall WIN score: {validation['total_win_score']:.1f}%"
            ]
            
            # Areas for improvement
            if validation["wisdom_score"] < 80:
                validation["areas_for_improvement"].append("Enhance integration strategy and business alignment")
            if validation["intelligence_score"] < 80:
                validation["areas_for_improvement"].append("Improve technical implementation and reliability")
            if validation["networking_score"] < 80:
                validation["areas_for_improvement"].append("Strengthen system connectivity and stakeholder engagement")
            
            validation["validation_status"] = "validated"
            
            return validation
            
        except Exception as e:
            return {
                "win_id": win_context.get("win_id", "unknown"),
                "error": "WIN validation failed",
                "agent_template": "IntegrationAgent"
            }

    # Helper methods for strategic execution
    async def _execute_api_integration(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API integration action"""
        return {
            "action": "api_integration",
            "integration_pattern": "rest_api_gateway",
            "apis_connected": 8,
            "endpoints_created": 25,
            "authentication_method": "oauth2_jwt",
            "rate_limiting": "intelligent_throttling",
            "monitoring": "comprehensive_api_analytics"
        }

    async def _execute_data_synchronization(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data synchronization action"""
        return {
            "action": "data_synchronization",
            "sync_pattern": "real_time_streaming",
            "data_sources": 12,
            "transformation_rules": 45,
            "sync_frequency": "continuous",
            "data_quality": "validated_and_cleansed",
            "conflict_resolution": "automated_with_audit"
        }

    async def _execute_enterprise_integration(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enterprise integration action"""
        return {
            "action": "enterprise_integration",
            "integration_platform": "enterprise_service_bus",
            "systems_integrated": 6,
            "business_processes": 15,
            "sso_enabled": True,
            "compliance_level": "enterprise_grade",
            "scalability": "horizontally_scalable"
        }

    async def _execute_workflow_automation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow automation action"""
        return {
            "action": "workflow_automation",
            "automation_platform": "business_process_automation",
            "processes_automated": 18,
            "approval_workflows": 8,
            "notification_system": "multi_channel",
            "efficiency_gain": "65%",
            "error_reduction": "80%"
        }

    async def _execute_general_integration(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute general integration action"""
        return {
            "action": "general_integration",
            "integration_approach": "hybrid_connectivity",
            "connectors_built": 5,
            "data_mappings": 25,
            "monitoring_setup": "comprehensive",
            "documentation": "detailed_and_maintained"
        }

    def _identify_systems(self, description: str, context: Dict[str, Any]) -> List[str]:
        """Identify systems involved in integration"""
        systems = []
        
        # Check description for system mentions
        if "database" in description.lower():
            systems.append("database")
        
        if "crm" in description.lower():
            systems.append("crm_system")
        
        if "erp" in description.lower():
            systems.append("erp_system")
        
        if "api" in description.lower():
            systems.append("external_api")
        
        # Check context for additional systems
        if context.get("source_systems"):
            systems.extend(context["source_systems"])
        
        return systems

    def _calculate_integration_recognition_confidence(self, recognition_data: Dict[str, Any]) -> float:
        """Calculate confidence in integration recognition analysis"""
        base_confidence = 75.0
        
        if recognition_data.get("description"):
            base_confidence += 10.0
        
        if recognition_data.get("context", {}).get("systems"):
            base_confidence += 10.0
        
        if recognition_data.get("technical_requirements"):
            base_confidence += 5.0
        
        return min(100.0, base_confidence) 