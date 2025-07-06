"""
TensionAnalyzer - Core component for intelligent tension analysis

Analyzes tensions to:
- Classify tension types (Problem, Opportunity, Risk, Conflict, Idea)
- Extract key patterns and themes
- Assess impact and urgency
- Identify relationships between tensions
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TensionType(Enum):
    PROBLEM = "Problem"
    OPPORTUNITY = "Opportunity" 
    RISK = "Risk"
    CONFLICT = "Conflict"
    IDEA = "Idea"
    UNKNOWN = "Unknown"

class ImpactLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class UrgencyLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class TensionAnalysis:
    """Kết quả phân tích tension"""
    tension_type: TensionType
    impact_level: ImpactLevel
    urgency_level: UrgencyLevel
    confidence_score: float  # 0.0 - 1.0
    key_themes: List[str]
    extracted_entities: List[str]
    suggested_priority: int  # 0-2 (normal, high, critical)
    reasoning: str

class TensionAnalyzer:
    """
    AI-powered tension analyzer using rule-based pattern matching.
    
    This is the MVP version focusing on:
    - Pattern recognition in tension descriptions
    - Rule-based classification
    - Impact/urgency assessment
    - Key theme extraction
    """
    
    def __init__(self):
        self._initialize_patterns()
        self._initialize_keywords()
    
    def _initialize_patterns(self):
        """Initialize regex patterns for tension analysis"""
        self.problem_patterns = [
            r'\b(lỗi|bug|sự cố|vấn đề|thất bại|không hoạt động|bị hỏng)\b',
            r'\b(error|failure|issue|problem|broken|not working)\b',
            r'\b(thiếu|mất|không có|không đủ)\b',
            r'\b(missing|lack|insufficient|absent)\b'
        ]
        
        self.opportunity_patterns = [
            r'\b(cơ hội|tiềm năng|có thể|nên|khả năng)\b',
            r'\b(opportunity|potential|could|should|possibility)\b',
            r'\b(cải thiện|tối ưu|nâng cao|phát triển)\b',
            r'\b(improve|optimize|enhance|develop|growth)\b'
        ]
        
        self.risk_patterns = [
            r'\b(rủi ro|nguy hiểm|có thể|lo ngại|đe dọa)\b',
            r'\b(risk|danger|threat|concern|vulnerability)\b',
            r'\b(nếu không|có thể dẫn đến|sẽ gây ra)\b',
            r'\b(if not|might lead to|could cause)\b'
        ]
        
        self.conflict_patterns = [
            r'\b(xung đột|mâu thuẫn|bất đồng|tranh cãi)\b',
            r'\b(conflict|disagreement|dispute|tension|clash)\b',
            r'\b(không đồng ý|phản đối|khác biệt)\b',
            r'\b(disagree|oppose|different|contradiction)\b'
        ]
        
        self.idea_patterns = [
            r'\b(ý tưởng|đề xuất|gợi ý|sáng kiến)\b',
            r'\b(idea|suggestion|proposal|initiative)\b',
            r'\b(có thể thử|nên làm|đề nghị)\b',
            r'\b(could try|should do|propose|recommend)\b'
        ]
    
    def _initialize_keywords(self):
        """Initialize keyword dictionaries for impact/urgency assessment"""
        self.high_impact_keywords = [
            'khách hàng', 'customer', 'doanh thu', 'revenue', 'hệ thống', 'system',
            'bảo mật', 'security', 'dữ liệu', 'data', 'sản phẩm', 'product',
            'chiến lược', 'strategy', 'tài chính', 'financial'
        ]
        
        self.high_urgency_keywords = [
            'ngay lập tức', 'immediately', 'khẩn cấp', 'urgent', 'gấp', 'asap',
            'deadline', 'hạn chót', 'sớm nhất', 'critical', 'quan trọng',
            'production', 'sản xuất', 'live', 'trực tiếp'
        ]
        
        self.critical_keywords = [
            'sập', 'crash', 'down', 'mất dữ liệu', 'data loss', 'hack', 'tấn công',
            'attack', 'rò rỉ', 'leak', 'vi phạm', 'breach', 'pháp lý', 'legal'
        ]
    
    def analyze_tension(self, title: str, description: str, 
                       current_status: str = "Open") -> TensionAnalysis:
        """
        Phân tích tension và trả về kết quả chi tiết
        
        Args:
            title: Tiêu đề tension
            description: Mô tả chi tiết tension
            current_status: Trạng thái hiện tại
            
        Returns:
            TensionAnalysis object với kết quả phân tích
        """
        # Combine title and description for analysis
        full_text = f"{title} {description}".lower()
        
        # Classify tension type
        tension_type, type_confidence = self._classify_tension_type(full_text)
        
        # Assess impact and urgency
        impact_level = self._assess_impact(full_text)
        urgency_level = self._assess_urgency(full_text)
        
        # Extract themes and entities
        key_themes = self._extract_themes(full_text)
        extracted_entities = self._extract_entities(full_text)
        
        # Calculate suggested priority
        suggested_priority = self._calculate_priority(impact_level, urgency_level)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            tension_type, impact_level, urgency_level, 
            key_themes, type_confidence
        )
        
        return TensionAnalysis(
            tension_type=tension_type,
            impact_level=impact_level,
            urgency_level=urgency_level,
            confidence_score=type_confidence,
            key_themes=key_themes,
            extracted_entities=extracted_entities,
            suggested_priority=suggested_priority,
            reasoning=reasoning
        )
    
    def _classify_tension_type(self, text: str) -> Tuple[TensionType, float]:
        """Classify tension type using pattern matching"""
        scores = {
            TensionType.PROBLEM: self._count_pattern_matches(text, self.problem_patterns),
            TensionType.OPPORTUNITY: self._count_pattern_matches(text, self.opportunity_patterns),
            TensionType.RISK: self._count_pattern_matches(text, self.risk_patterns),
            TensionType.CONFLICT: self._count_pattern_matches(text, self.conflict_patterns),
            TensionType.IDEA: self._count_pattern_matches(text, self.idea_patterns)
        }
        
        if all(score == 0 for score in scores.values()):
            return TensionType.UNKNOWN, 0.5
        
        best_type = max(scores, key=scores.get)
        max_score = scores[best_type]
        total_score = sum(scores.values())
        
        confidence = max_score / total_score if total_score > 0 else 0.5
        
        return best_type, min(confidence, 0.95)  # Cap confidence at 95%
    
    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Count pattern matches in text"""
        count = 0
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            count += matches
        return count
    
    def _assess_impact(self, text: str) -> ImpactLevel:
        """Assess impact level based on keywords"""
        critical_count = sum(1 for keyword in self.critical_keywords if keyword in text)
        high_count = sum(1 for keyword in self.high_impact_keywords if keyword in text)
        
        if critical_count > 0:
            return ImpactLevel.CRITICAL
        elif high_count >= 2:
            return ImpactLevel.HIGH
        elif high_count == 1:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
    
    def _assess_urgency(self, text: str) -> UrgencyLevel:
        """Assess urgency level based on keywords"""
        critical_count = sum(1 for keyword in self.critical_keywords if keyword in text)
        urgent_count = sum(1 for keyword in self.high_urgency_keywords if keyword in text)
        
        if critical_count > 0:
            return UrgencyLevel.CRITICAL
        elif urgent_count >= 2:
            return UrgencyLevel.HIGH
        elif urgent_count == 1:
            return UrgencyLevel.MEDIUM
        else:
            return UrgencyLevel.LOW
    
    def _extract_themes(self, text: str) -> List[str]:
        """Extract key themes from text"""
        themes = []
        
        # Technology themes
        if re.search(r'\b(api|database|server|code|bug|system)\b', text):
            themes.append("Technology")
        
        # Business themes  
        if re.search(r'\b(customer|revenue|business|market|strategy)\b', text):
            themes.append("Business")
        
        # Process themes
        if re.search(r'\b(process|workflow|procedure|method)\b', text):
            themes.append("Process")
        
        # People themes
        if re.search(r'\b(team|user|staff|people|human)\b', text):
            themes.append("People")
        
        # Security themes
        if re.search(r'\b(security|breach|hack|vulnerability|attack)\b', text):
            themes.append("Security")
        
        return themes or ["General"]
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract key entities (simplified NER)"""
        entities = []
        
        # Find potential system/service names (capitalized words)
        system_matches = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b', text)
        entities.extend(system_matches[:5])  # Limit to 5 entities
        
        return entities
    
    def _calculate_priority(self, impact: ImpactLevel, urgency: UrgencyLevel) -> int:
        """Calculate priority based on impact and urgency matrix"""
        # Priority matrix: 0=normal, 1=high, 2=critical
        if impact == ImpactLevel.CRITICAL or urgency == UrgencyLevel.CRITICAL:
            return 2  # Critical
        elif impact == ImpactLevel.HIGH and urgency == UrgencyLevel.HIGH:
            return 2  # Critical
        elif impact == ImpactLevel.HIGH or urgency == UrgencyLevel.HIGH:
            return 1  # High
        elif impact == ImpactLevel.MEDIUM and urgency == UrgencyLevel.MEDIUM:
            return 1  # High
        else:
            return 0  # Normal
    
    def _generate_reasoning(self, tension_type: TensionType, impact: ImpactLevel, 
                          urgency: UrgencyLevel, themes: List[str], 
                          confidence: float) -> str:
        """Generate human-readable reasoning for the analysis"""
        reasoning_parts = []
        
        # Type classification
        reasoning_parts.append(
            f"Classified as {tension_type.value} with {confidence:.1%} confidence"
        )
        
        # Impact and urgency
        reasoning_parts.append(
            f"Impact: {impact.name}, Urgency: {urgency.name}"
        )
        
        # Themes
        if themes:
            reasoning_parts.append(f"Key themes: {', '.join(themes)}")
        
        # Priority justification
        priority = self._calculate_priority(impact, urgency)
        priority_names = {0: "Normal", 1: "High", 2: "Critical"}
        reasoning_parts.append(
            f"Suggested priority: {priority_names[priority]} based on impact/urgency matrix"
        )
        
        return ". ".join(reasoning_parts) + "." 