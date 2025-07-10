"""
TRM-OS: Failure Lesson Extractor
Trích xuất và học từ failures để cải thiện hệ thống
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class FailureType(Enum):
    """Các loại failure có thể xảy ra"""
    STRATEGIC = "strategic"
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    COMMUNICATION = "communication"
    RESOURCE = "resource"
    TIMING = "timing"

class FailureSeverity(Enum):
    """Mức độ nghiêm trọng của failure"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FailureLesson:
    """Bài học từ failure"""
    failure_id: str
    failure_type: FailureType
    severity: FailureSeverity
    description: str
    root_cause: str
    lessons_learned: List[str]
    prevention_actions: List[str]
    detection_methods: List[str]
    recovery_procedures: List[str]
    confidence_score: float
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FailurePattern:
    """Pattern của failures"""
    pattern_id: str
    pattern_name: str
    failure_types: List[FailureType]
    common_indicators: List[str]
    frequency: int
    impact_score: float
    prevention_strategies: List[str]
    early_warning_signs: List[str]
    mitigation_steps: List[str]

class FailureLessonExtractor:
    """
    Hệ thống trích xuất và học từ failures
    Tuân thủ AGE v2.0 philosophy: Learning from failures để improve WINs
    """
    
    def __init__(self):
        self.lessons_database: Dict[str, FailureLesson] = {}
        self.patterns_database: Dict[str, FailurePattern] = {}
        self.learning_history: List[Dict[str, Any]] = []
        
        # Analysis thresholds
        self.pattern_detection_threshold = 0.7
        self.lesson_confidence_threshold = 0.8
        self.improvement_tracking_window = 30  # days
        
        logger.info("FailureLessonExtractor initialized với advanced learning capabilities")

    async def extract_lessons_from_failure(self, 
                                         failure_event: Dict[str, Any]) -> FailureLesson:
        """
        Trích xuất lessons từ failure event
        
        Args:
            failure_event: Event failure cần phân tích
            
        Returns:
            FailureLesson object với insights
        """
        try:
            # 1. Phân tích failure type
            failure_type = await self._classify_failure_type(failure_event)
            
            # 2. Đánh giá severity
            severity = await self._assess_failure_severity(failure_event)
            
            # 3. Root cause analysis
            root_cause = await self._analyze_root_cause(failure_event)
            
            # 4. Trích xuất lessons
            lessons = await self._extract_core_lessons(failure_event, root_cause)
            
            # 5. Xác định prevention actions
            prevention_actions = await self._identify_prevention_actions(
                failure_event, root_cause, lessons
            )
            
            # 6. Detection methods
            detection_methods = await self._develop_detection_methods(failure_event)
            
            # 7. Recovery procedures
            recovery_procedures = await self._create_recovery_procedures(failure_event)
            
            # 8. Tính confidence score
            confidence_score = await self._calculate_confidence_score(
                failure_event, lessons, prevention_actions
            )
            
            failure_lesson = FailureLesson(
                failure_id=failure_event.get('id', f"failure_{datetime.now().timestamp()}"),
                failure_type=failure_type,
                severity=severity,
                description=failure_event.get('description', ''),
                root_cause=root_cause,
                lessons_learned=lessons,
                prevention_actions=prevention_actions,
                detection_methods=detection_methods,
                recovery_procedures=recovery_procedures,
                confidence_score=confidence_score,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata=failure_event.get('metadata', {})
            )
            
            # Store lesson
            self.lessons_database[failure_lesson.failure_id] = failure_lesson
            
            # Update patterns
            await self._update_failure_patterns(failure_lesson)
            
            logger.info(f"Extracted lesson từ failure {failure_lesson.failure_id} "
                       f"với confidence {confidence_score:.2f}")
            
            return failure_lesson
            
        except Exception as e:
            logger.error(f"Error extracting lessons từ failure: {e}")
            raise

    async def _classify_failure_type(self, failure_event: Dict[str, Any]) -> FailureType:
        """Phân loại loại failure"""
        try:
            # Keywords cho từng loại failure
            type_keywords = {
                FailureType.STRATEGIC: ['goal', 'objective', 'strategy', 'direction', 'vision'],
                FailureType.TECHNICAL: ['error', 'exception', 'bug', 'system', 'code'],
                FailureType.OPERATIONAL: ['process', 'workflow', 'operation', 'procedure'],
                FailureType.COMMUNICATION: ['message', 'communication', 'notification', 'sync'],
                FailureType.RESOURCE: ['memory', 'cpu', 'disk', 'network', 'quota'],
                FailureType.TIMING: ['timeout', 'deadline', 'schedule', 'timing', 'delay']
            }
            
            description = failure_event.get('description', '').lower()
            error_message = failure_event.get('error_message', '').lower()
            context = f"{description} {error_message}"
            
            # Score cho từng type
            type_scores = {}
            for failure_type, keywords in type_keywords.items():
                score = sum(1 for keyword in keywords if keyword in context)
                type_scores[failure_type] = score
            
            # Chọn type với score cao nhất
            if type_scores:
                best_type = max(type_scores, key=type_scores.get)
                if type_scores[best_type] > 0:
                    return best_type
            
            # Default fallback
            return FailureType.TECHNICAL
            
        except Exception as e:
            logger.warning(f"Error classifying failure type: {e}")
            return FailureType.TECHNICAL

    async def _assess_failure_severity(self, failure_event: Dict[str, Any]) -> FailureSeverity:
        """Đánh giá mức độ nghiêm trọng"""
        try:
            severity_indicators = {
                FailureSeverity.CRITICAL: ['critical', 'fatal', 'emergency', 'system down', 'data loss'],
                FailureSeverity.HIGH: ['high', 'major', 'significant', 'important', 'urgent'],
                FailureSeverity.MEDIUM: ['medium', 'moderate', 'warning', 'attention'],
                FailureSeverity.LOW: ['low', 'minor', 'info', 'notice', 'trivial']
            }
            
            description = failure_event.get('description', '').lower()
            error_message = failure_event.get('error_message', '').lower()
            context = f"{description} {error_message}"
            
            # Check từ critical xuống low
            for severity in [FailureSeverity.CRITICAL, FailureSeverity.HIGH, 
                           FailureSeverity.MEDIUM, FailureSeverity.LOW]:
                indicators = severity_indicators[severity]
                if any(indicator in context for indicator in indicators):
                    return severity
            
            # Impact-based assessment
            impact_score = failure_event.get('impact_score', 0)
            if impact_score >= 0.8:
                return FailureSeverity.CRITICAL
            elif impact_score >= 0.6:
                return FailureSeverity.HIGH
            elif impact_score >= 0.3:
                return FailureSeverity.MEDIUM
            else:
                return FailureSeverity.LOW
                
        except Exception as e:
            logger.warning(f"Error assessing failure severity: {e}")
            return FailureSeverity.MEDIUM

    async def _analyze_root_cause(self, failure_event: Dict[str, Any]) -> str:
        """Phân tích root cause của failure"""
        try:
            # Root cause analysis framework
            potential_causes = []
            
            # 1. Technical causes
            if 'error_message' in failure_event:
                error_msg = failure_event['error_message']
                if 'connection' in error_msg.lower():
                    potential_causes.append("Network connectivity issues")
                elif 'timeout' in error_msg.lower():
                    potential_causes.append("Performance bottleneck or resource exhaustion")
                elif 'permission' in error_msg.lower():
                    potential_causes.append("Access control or authentication failure")
                elif 'not found' in error_msg.lower():
                    potential_causes.append("Resource or configuration missing")
            
            # 2. Context-based causes
            context = failure_event.get('context', {})
            if context.get('high_load', False):
                potential_causes.append("System overload during peak usage")
            if context.get('recent_deployment', False):
                potential_causes.append("Recent code changes or configuration updates")
            if context.get('external_dependency_failure', False):
                potential_causes.append("External service dependency failure")
            
            # 3. Pattern-based causes
            similar_failures = await self._find_similar_failures(failure_event)
            if similar_failures:
                common_causes = [f.root_cause for f in similar_failures if f.root_cause]
                if common_causes:
                    potential_causes.extend(common_causes)
            
            # Synthesize root cause
            if potential_causes:
                # Chọn cause phổ biến nhất hoặc đầu tiên
                root_cause = max(set(potential_causes), key=potential_causes.count)
            else:
                root_cause = f"Unknown root cause - requires deeper investigation for {failure_event.get('type', 'failure')}"
            
            return root_cause
            
        except Exception as e:
            logger.warning(f"Error analyzing root cause: {e}")
            return "Root cause analysis incomplete - manual investigation required"

    async def _extract_core_lessons(self, 
                                  failure_event: Dict[str, Any], 
                                  root_cause: str) -> List[str]:
        """Trích xuất core lessons từ failure"""
        try:
            lessons = []
            
            # 1. Technical lessons
            if 'error_message' in failure_event:
                lessons.append(f"Error handling cần improve cho: {failure_event['error_message']}")
            
            # 2. Process lessons
            if 'process_breakdown' in failure_event.get('context', {}):
                lessons.append("Quy trình cần được review và strengthen")
            
            # 3. Monitoring lessons
            if failure_event.get('detection_time', 0) > 300:  # 5 minutes
                lessons.append("Monitoring và alerting cần được enhance cho faster detection")
            
            # 4. Recovery lessons
            if failure_event.get('recovery_time', 0) > 600:  # 10 minutes
                lessons.append("Recovery procedures cần được optimize cho faster restoration")
            
            # 5. Root cause specific lessons
            if 'network' in root_cause.lower():
                lessons.append("Network resilience và retry mechanisms cần strengthen")
            elif 'performance' in root_cause.lower():
                lessons.append("Performance monitoring và auto-scaling cần implement")
            elif 'configuration' in root_cause.lower():
                lessons.append("Configuration management và validation cần improve")
            
            # 6. Prevention lessons
            lessons.append(f"Implement proactive measures để prevent: {root_cause}")
            
            # 7. Learning lessons
            lessons.append("System cần adapt từ failure này để avoid similar issues")
            
            return lessons
            
        except Exception as e:
            logger.warning(f"Error extracting core lessons: {e}")
            return ["General lesson: Learn từ failure này để improve system resilience"]

    async def _identify_prevention_actions(self, 
                                         failure_event: Dict[str, Any],
                                         root_cause: str,
                                         lessons: List[str]) -> List[str]:
        """Xác định các hành động prevention"""
        try:
            actions = []
            
            # 1. Monitoring actions
            actions.append("Enhance monitoring cho early detection của similar issues")
            actions.append("Implement automated alerts cho key failure indicators")
            
            # 2. Technical actions
            if 'error' in root_cause.lower():
                actions.append("Implement robust error handling và graceful degradation")
                actions.append("Add comprehensive logging cho better troubleshooting")
            
            # 3. Process actions
            actions.append("Review và update operational procedures")
            actions.append("Conduct regular failure scenario testing")
            
            # 4. Root cause specific actions
            if 'network' in root_cause.lower():
                actions.append("Implement network redundancy và failover mechanisms")
                actions.append("Add network health monitoring và automatic retry logic")
            elif 'performance' in root_cause.lower():
                actions.append("Implement auto-scaling và load balancing")
                actions.append("Add performance baselines và threshold monitoring")
            elif 'configuration' in root_cause.lower():
                actions.append("Implement configuration validation và automated testing")
                actions.append("Add configuration change tracking và rollback capabilities")
            
            # 5. Learning actions
            actions.append("Update system knowledge base với lessons learned")
            actions.append("Train agents để recognize và prevent similar patterns")
            
            return actions
            
        except Exception as e:
            logger.warning(f"Error identifying prevention actions: {e}")
            return ["Implement general failure prevention measures"]

    async def _develop_detection_methods(self, failure_event: Dict[str, Any]) -> List[str]:
        """Phát triển methods để detect similar failures early"""
        try:
            methods = []
            
            # 1. Monitoring methods
            methods.append("Real-time system health monitoring với anomaly detection")
            methods.append("Key performance indicator (KPI) tracking và alerting")
            
            # 2. Pattern-based detection
            if 'pattern' in failure_event.get('metadata', {}):
                methods.append("Pattern recognition algorithms cho failure prediction")
            
            # 3. Threshold-based detection
            methods.append("Dynamic threshold monitoring với machine learning")
            methods.append("Trend analysis cho early warning indicators")
            
            # 4. Dependency monitoring
            methods.append("External dependency health checks và failover detection")
            methods.append("Resource utilization monitoring với predictive alerts")
            
            # 5. User impact detection
            methods.append("User experience monitoring cho impact assessment")
            methods.append("Business metric tracking cho early business impact detection")
            
            return methods
            
        except Exception as e:
            logger.warning(f"Error developing detection methods: {e}")
            return ["Implement comprehensive monitoring và alerting systems"]

    async def _create_recovery_procedures(self, failure_event: Dict[str, Any]) -> List[str]:
        """Tạo recovery procedures"""
        try:
            procedures = []
            
            # 1. Immediate response
            procedures.append("Immediate incident assessment và impact evaluation")
            procedures.append("Stakeholder notification với clear communication")
            
            # 2. Containment
            procedures.append("Isolate affected components để prevent spread")
            procedures.append("Implement temporary workarounds nếu available")
            
            # 3. Recovery
            procedures.append("Execute systematic recovery steps với checkpoints")
            procedures.append("Verify system functionality sau recovery")
            
            # 4. Validation
            procedures.append("Run comprehensive tests để ensure full recovery")
            procedures.append("Monitor system stability trong extended period")
            
            # 5. Learning
            procedures.append("Document recovery process với lessons learned")
            procedures.append("Update recovery procedures based on experience")
            
            return procedures
            
        except Exception as e:
            logger.warning(f"Error creating recovery procedures: {e}")
            return ["Follow standard incident response và recovery procedures"]

    async def _calculate_confidence_score(self, 
                                        failure_event: Dict[str, Any],
                                        lessons: List[str],
                                        prevention_actions: List[str]) -> float:
        """Tính confidence score cho lesson extraction"""
        try:
            confidence_factors = []
            
            # 1. Data completeness
            data_completeness = 0
            required_fields = ['description', 'error_message', 'timestamp', 'context']
            available_fields = sum(1 for field in required_fields if field in failure_event)
            data_completeness = available_fields / len(required_fields)
            confidence_factors.append(data_completeness * 0.3)
            
            # 2. Analysis depth
            analysis_depth = 0
            if len(lessons) >= 5:
                analysis_depth += 0.3
            if len(prevention_actions) >= 5:
                analysis_depth += 0.3
            if failure_event.get('root_cause_analysis', False):
                analysis_depth += 0.4
            confidence_factors.append(min(analysis_depth, 1.0) * 0.3)
            
            # 3. Historical patterns
            similar_failures = await self._find_similar_failures(failure_event)
            pattern_confidence = min(len(similar_failures) / 5, 1.0)
            confidence_factors.append(pattern_confidence * 0.2)
            
            # 4. Validation potential
            validation_score = 0.8  # Default high confidence trong validation
            confidence_factors.append(validation_score * 0.2)
            
            total_confidence = sum(confidence_factors)
            return round(total_confidence, 3)
            
        except Exception as e:
            logger.warning(f"Error calculating confidence score: {e}")
            return 0.7  # Default medium confidence

    async def _find_similar_failures(self, failure_event: Dict[str, Any]) -> List[FailureLesson]:
        """Tìm similar failures trong database"""
        try:
            similar_failures = []
            
            for lesson in self.lessons_database.values():
                similarity_score = await self._calculate_similarity(failure_event, lesson)
                if similarity_score >= self.pattern_detection_threshold:
                    similar_failures.append(lesson)
            
            return similar_failures
            
        except Exception as e:
            logger.warning(f"Error finding similar failures: {e}")
            return []

    async def _calculate_similarity(self, 
                                  failure_event: Dict[str, Any], 
                                  lesson: FailureLesson) -> float:
        """Tính similarity giữa failure event và lesson"""
        try:
            similarity_factors = []
            
            # 1. Type similarity
            event_type = await self._classify_failure_type(failure_event)
            type_similarity = 1.0 if event_type == lesson.failure_type else 0.0
            similarity_factors.append(type_similarity * 0.4)
            
            # 2. Description similarity (simple keyword matching)
            event_desc = failure_event.get('description', '').lower()
            lesson_desc = lesson.description.lower()
            common_words = set(event_desc.split()) & set(lesson_desc.split())
            desc_similarity = len(common_words) / max(len(event_desc.split()), 1)
            similarity_factors.append(min(desc_similarity, 1.0) * 0.3)
            
            # 3. Context similarity
            event_context = failure_event.get('context', {})
            lesson_context = lesson.metadata.get('context', {})
            context_keys = set(event_context.keys()) & set(lesson_context.keys())
            context_similarity = len(context_keys) / max(len(event_context), 1) if event_context else 0
            similarity_factors.append(min(context_similarity, 1.0) * 0.3)
            
            return sum(similarity_factors)
            
        except Exception as e:
            logger.warning(f"Error calculating similarity: {e}")
            return 0.0

    async def _update_failure_patterns(self, lesson: FailureLesson):
        """Update failure patterns với new lesson"""
        try:
            # Tìm existing pattern hoặc tạo mới
            pattern_key = f"{lesson.failure_type.value}_{lesson.severity.value}"
            
            if pattern_key in self.patterns_database:
                pattern = self.patterns_database[pattern_key]
                pattern.frequency += 1
                pattern.impact_score = (pattern.impact_score + lesson.confidence_score) / 2
            else:
                pattern = FailurePattern(
                    pattern_id=pattern_key,
                    pattern_name=f"{lesson.failure_type.value.title()} {lesson.severity.value.title()} Failures",
                    failure_types=[lesson.failure_type],
                    common_indicators=lesson.detection_methods[:3],
                    frequency=1,
                    impact_score=lesson.confidence_score,
                    prevention_strategies=lesson.prevention_actions[:3],
                    early_warning_signs=lesson.detection_methods[:2],
                    mitigation_steps=lesson.recovery_procedures[:3]
                )
                self.patterns_database[pattern_key] = pattern
            
            logger.info(f"Updated failure pattern {pattern_key} với frequency {pattern.frequency}")
            
        except Exception as e:
            logger.warning(f"Error updating failure patterns: {e}")

    async def get_lessons_by_type(self, failure_type: FailureType) -> List[FailureLesson]:
        """Lấy lessons theo failure type"""
        return [lesson for lesson in self.lessons_database.values() 
                if lesson.failure_type == failure_type]

    async def get_high_confidence_lessons(self) -> List[FailureLesson]:
        """Lấy lessons với high confidence"""
        return [lesson for lesson in self.lessons_database.values()
                if lesson.confidence_score >= self.lesson_confidence_threshold]

    async def get_recent_lessons(self, days: int = 30) -> List[FailureLesson]:
        """Lấy lessons recent"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [lesson for lesson in self.lessons_database.values()
                if lesson.created_at >= cutoff_date]

    async def get_failure_patterns(self) -> List[FailurePattern]:
        """Lấy tất cả failure patterns"""
        return list(self.patterns_database.values())

    async def generate_improvement_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations dựa trên failure lessons"""
        try:
            recommendations = {
                'immediate_actions': [],
                'strategic_improvements': [],
                'monitoring_enhancements': [],
                'process_updates': [],
                'training_needs': []
            }
            
            # Analyze high-frequency patterns
            frequent_patterns = [p for p in self.patterns_database.values() if p.frequency >= 3]
            
            for pattern in frequent_patterns:
                recommendations['immediate_actions'].extend(pattern.prevention_strategies[:2])
                recommendations['monitoring_enhancements'].extend(pattern.early_warning_signs[:2])
            
            # Analyze high-confidence lessons
            high_conf_lessons = await self.get_high_confidence_lessons()
            
            for lesson in high_conf_lessons[-10:]:  # Latest 10 high-confidence lessons
                recommendations['strategic_improvements'].extend(lesson.prevention_actions[:2])
                recommendations['process_updates'].extend(lesson.recovery_procedures[:2])
            
            # Remove duplicates
            for key in recommendations:
                recommendations[key] = list(set(recommendations[key]))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating improvement recommendations: {e}")
            return {}

    def get_system_status(self) -> Dict[str, Any]:
        """Lấy system status"""
        return {
            'total_lessons': len(self.lessons_database),
            'total_patterns': len(self.patterns_database),
            'high_confidence_lessons': len([l for l in self.lessons_database.values() 
                                           if l.confidence_score >= self.lesson_confidence_threshold]),
            'recent_lessons_30d': len([l for l in self.lessons_database.values()
                                     if (datetime.now() - l.created_at).days <= 30]),
            'failure_types_distribution': {
                ft.value: len([l for l in self.lessons_database.values() if l.failure_type == ft])
                for ft in FailureType
            },
            'severity_distribution': {
                fs.value: len([l for l in self.lessons_database.values() if l.severity == fs])
                for fs in FailureSeverity
            }
        } 