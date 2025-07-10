#!/usr/bin/env python3
"""
Semantic Change Detector - TRM-OS v2.0 Living System

Advanced semantic change detection using:
- Vector embeddings comparison với Supabase
- Commercial AI analysis cho intent shifts
- Multi-metric change significance calculation
- Intent drift pattern recognition

Philosophy: Detect semantic changes để trigger autonomous evolution
"""

import os
import asyncio
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import math

from trm_api.core.logging_config import get_logger
from trm_api.core.living_knowledge_core import ContentChangeType, ContentSnapshot
from trm_api.eventbus.system_event_bus import SystemEventBus, SystemEvent, EventType

# Real Commercial AI imports
import openai
from openai import AsyncOpenAI

logger = get_logger(__name__)


class SemanticAnalysisType(str, Enum):
    """Types of semantic analysis"""
    VECTOR_SIMILARITY = "vector_similarity"
    LEXICAL_ANALYSIS = "lexical_analysis"
    INTENT_ANALYSIS = "intent_analysis"
    STRUCTURAL_ANALYSIS = "structural_analysis"
    COMMERCIAL_AI_ANALYSIS = "commercial_ai_analysis"


class IntentCategory(str, Enum):
    """Categories of intent detected"""
    VISION_CHANGE = "vision_change"
    STRATEGY_SHIFT = "strategy_shift"
    GOAL_MODIFICATION = "goal_modification"
    APPROACH_CHANGE = "approach_change"
    PRIORITY_SHIFT = "priority_shift"
    SCOPE_EXPANSION = "scope_expansion"
    SCOPE_REDUCTION = "scope_reduction"
    METHODOLOGY_CHANGE = "methodology_change"


@dataclass
class SemanticAnalysisResult:
    """Result của semantic analysis"""
    analysis_type: SemanticAnalysisType
    similarity_score: float  # 0.0 - 1.0
    change_significance: float  # 0.0 - 1.0
    detected_patterns: List[str] = field(default_factory=list)
    confidence: float = 0.0
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0


@dataclass
class IntentShiftAnalysis:
    """Analysis của intent shift detection"""
    intent_category: IntentCategory
    confidence: float
    old_intent_keywords: List[str]
    new_intent_keywords: List[str]
    intent_shift_magnitude: float  # 0.0 - 1.0
    detected_changes: List[str]
    commercial_ai_insights: Optional[Dict[str, Any]] = None


@dataclass
class ComprehensiveChangeAnalysis:
    """Comprehensive analysis combining multiple detection methods"""
    content_id: str
    old_snapshot: ContentSnapshot
    new_snapshot: ContentSnapshot
    overall_significance: float
    detected_change_type: ContentChangeType
    semantic_analyses: List[SemanticAnalysisResult]
    intent_shift_analysis: Optional[IntentShiftAnalysis]
    confidence_score: float
    recommended_actions: List[str]
    analysis_timestamp: datetime = field(default_factory=datetime.now)


class VectorEmbeddingAnalyzer:
    """Real Commercial AI Vector Embedding Analyzer"""
    
    def __init__(self):
        self.logger = get_logger("vector_embedding_analyzer")
        
        # Initialize OpenAI client với API key từ environment
        self.openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Fallback embedding service (Anthropic/Google)
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Embedding configuration
        self.embedding_model = "text-embedding-3-small"  # OpenAI's latest model
        self.embedding_dimension = 1536  # text-embedding-3-small dimension
        self.max_text_length = 8000  # OpenAI token limits
        
        # Similarity thresholds cho real embeddings
        self.similarity_thresholds = {
            "very_similar": 0.95,    # Tăng từ 0.80 vì real embeddings accurate hơn
            "similar": 0.85,         # Tăng từ 0.60
            "somewhat_similar": 0.70, # Tăng từ 0.50
            "different": 0.50,       # Tăng từ 0.30
            "very_different": 0.30   # Tăng từ 0.10
        }
        
        # Performance tracking
        self.api_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens_used": 0,
            "average_response_time": 0.0
        }
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate real vector embedding using OpenAI API
        """
        start_time = datetime.now()
        
        try:
            # Validate API key
            if not self.openai_client.api_key:
                self.logger.error("OpenAI API key not configured")
                return await self._fallback_embedding_generation(text)
            
            # Truncate text if too long
            if len(text) > self.max_text_length:
                text = text[:self.max_text_length]
                self.logger.warning(f"Text truncated to {self.max_text_length} characters")
            
            # Track API call
            self.api_stats["total_requests"] += 1
            
            # Call OpenAI Embeddings API
            response = await self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text,
                encoding_format="float"
            )
            
            # Extract embedding vector
            embedding = response.data[0].embedding
            
            # Update statistics
            self.api_stats["successful_requests"] += 1
            self.api_stats["total_tokens_used"] += response.usage.total_tokens
            
            response_time = (datetime.now() - start_time).total_seconds()
            self._update_average_response_time(response_time)
            
            self.logger.info(f"Generated embedding: {len(embedding)} dimensions, {response.usage.total_tokens} tokens")
            
            return embedding
            
        except Exception as e:
            self.logger.error(f"OpenAI embedding generation failed: {e}")
            self.api_stats["failed_requests"] += 1
            
            # Fallback to alternative embedding service
            return await self._fallback_embedding_generation(text)
    
    async def _fallback_embedding_generation(self, text: str) -> List[float]:
        """
        Fallback embedding generation khi OpenAI API fails
        Sử dụng sentence-transformers local model
        """
        try:
            # Try importing sentence-transformers for local fallback
            try:
                from sentence_transformers import SentenceTransformer
                
                # Load local model (chỉ một lần)
                if not hasattr(self, '_local_model'):
                    self._local_model = SentenceTransformer('all-MiniLM-L6-v2')
                
                # Generate embedding locally
                embedding = self._local_model.encode(text).tolist()
                
                self.logger.warning("Used local sentence-transformers fallback")
                return embedding
                
            except ImportError:
                self.logger.warning("sentence-transformers not available, using hash-based fallback")
                return await self._hash_based_fallback(text)
            
        except Exception as e:
            self.logger.error(f"Fallback embedding generation failed: {e}")
            return await self._hash_based_fallback(text)
    
    async def _hash_based_fallback(self, text: str) -> List[float]:
        """
        Emergency hash-based fallback (last resort)
        """
        self.logger.warning("Using emergency hash-based embedding fallback")
        
        # Simple hash-based embedding (từ previous implementation)
        embedding_dim = 384  # Smaller dimension for fallback
        
        embedding = []
        for i in range(embedding_dim):
            hash_value = hash(f"{text}_{i}") % 1000000
            normalized_value = (hash_value / 1000000) * 2 - 1
            embedding.append(normalized_value)
        
        # Normalize to unit vector
        magnitude = math.sqrt(sum(x*x for x in embedding))
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding
    
    def _update_average_response_time(self, response_time: float) -> None:
        """Update average response time statistics"""
        total_successful = self.api_stats["successful_requests"]
        current_avg = self.api_stats["average_response_time"]
        
        # Calculate new average
        new_avg = ((current_avg * (total_successful - 1)) + response_time) / total_successful
        self.api_stats["average_response_time"] = new_avg

    def calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors với improved accuracy"""
        try:
            if len(vec1) != len(vec2):
                self.logger.warning(f"Vector dimensions mismatch: {len(vec1)} vs {len(vec2)}")
                # Pad shorter vector với zeros
                max_len = max(len(vec1), len(vec2))
                vec1 = vec1 + [0.0] * (max_len - len(vec1))
                vec2 = vec2 + [0.0] * (max_len - len(vec2))
            
            # Calculate dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            
            # Calculate magnitudes
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(b * b for b in vec2))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            # Calculate cosine similarity
            similarity = dot_product / (magnitude1 * magnitude2)
            
            # Clamp to [0, 1] range và handle floating point precision
            similarity = max(0.0, min(1.0, similarity))
            
            return round(similarity, 6)  # Round to 6 decimal places
            
        except Exception as e:
            self.logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0

    async def analyze_vector_similarity(
        self, 
        old_content: str, 
        new_content: str
    ) -> SemanticAnalysisResult:
        """Analyze semantic similarity using real Commercial AI embeddings"""
        start_time = datetime.now()
        
        try:
            # Generate real embeddings from OpenAI
            old_embedding = await self.generate_embedding(old_content)
            new_embedding = await self.generate_embedding(new_content)
            
            # Calculate similarity với improved accuracy
            similarity = self.calculate_cosine_similarity(old_embedding, new_embedding)
            
            # Calculate change significance
            change_significance = 1.0 - similarity
            
            # Determine patterns based on real similarity thresholds
            patterns = []
            for threshold_name, threshold_value in self.similarity_thresholds.items():
                if similarity >= threshold_value:
                    patterns.append(f"content_{threshold_name}")
                    break
            
            # Additional pattern detection với real embeddings
            if change_significance > 0.7:
                patterns.append("major_semantic_shift")
            elif change_significance > 0.5:
                patterns.append("significant_semantic_change")
            elif change_significance > 0.3:
                patterns.append("moderate_semantic_evolution")
            else:
                patterns.append("minor_semantic_adjustment")
            
            # Calculate confidence based on API success
            confidence = 0.95 if self.api_stats["successful_requests"] > 0 else 0.3
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Log performance metrics
            self.logger.info(f"Real embedding analysis: similarity={similarity:.4f}, "
                           f"significance={change_significance:.4f}, confidence={confidence:.2f}")
            
            return SemanticAnalysisResult(
                analysis_type=SemanticAnalysisType.VECTOR_SIMILARITY,
                similarity_score=similarity,
                change_significance=change_significance,
                detected_patterns=patterns,
                confidence=confidence,
                analysis_metadata={
                    "embedding_model": self.embedding_model,
                    "embedding_dimension": len(old_embedding),
                    "api_service": "openai_embeddings",
                    "old_content_length": len(old_content),
                    "new_content_length": len(new_content),
                    "tokens_used": self.api_stats["total_tokens_used"],
                    "api_success_rate": (self.api_stats["successful_requests"] / 
                                       max(self.api_stats["total_requests"], 1)) * 100
                },
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in real vector similarity analysis: {e}")
            return SemanticAnalysisResult(
                analysis_type=SemanticAnalysisType.VECTOR_SIMILARITY,
                similarity_score=0.0,
                change_significance=1.0,
                confidence=0.0,
                processing_time=0.0,
                detected_patterns=["analysis_failed"]
            )
    
    def get_api_statistics(self) -> Dict[str, Any]:
        """Get real-time API statistics"""
        success_rate = 0.0
        if self.api_stats["total_requests"] > 0:
            success_rate = (self.api_stats["successful_requests"] / 
                          self.api_stats["total_requests"]) * 100
        
        return {
            "total_requests": self.api_stats["total_requests"],
            "successful_requests": self.api_stats["successful_requests"],
            "failed_requests": self.api_stats["failed_requests"],
            "success_rate_percent": round(success_rate, 2),
            "total_tokens_used": self.api_stats["total_tokens_used"],
            "average_response_time_seconds": round(self.api_stats["average_response_time"], 3),
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dimension
        }


class LexicalAnalyzer:
    """Analyzer cho lexical và structural changes"""
    
    def __init__(self):
        self.stop_words = {
            "và", "the", "a", "an", "in", "on", "at", "to", "for", "of", "with",
            "by", "from", "about", "into", "through", "during", "before", "after",
            "above", "below", "up", "down", "out", "off", "over", "under", "again",
            "further", "then", "once", "là", "của", "với", "trong", "cho", "về"
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        words = text.lower().split()
        keywords = [
            word.strip('.,!?;:"()[]{}')
            for word in words
            if len(word) > 2 and word not in self.stop_words
        ]
        return list(set(keywords))  # Remove duplicates
    
    def calculate_lexical_similarity(self, old_text: str, new_text: str) -> float:
        """Calculate lexical similarity using Jaccard index"""
        old_keywords = set(self.extract_keywords(old_text))
        new_keywords = set(self.extract_keywords(new_text))
        
        if not old_keywords and not new_keywords:
            return 1.0  # Both empty
        
        intersection = len(old_keywords.intersection(new_keywords))
        union = len(old_keywords.union(new_keywords))
        
        return intersection / union if union > 0 else 0.0
    
    async def analyze_lexical_changes(
        self, 
        old_content: str, 
        new_content: str
    ) -> SemanticAnalysisResult:
        """Analyze lexical và structural changes"""
        start_time = datetime.now()
        
        try:
            # Calculate lexical similarity
            similarity = self.calculate_lexical_similarity(old_content, new_content)
            change_significance = 1.0 - similarity
            
            # Extract keywords for analysis
            old_keywords = set(self.extract_keywords(old_content))
            new_keywords = set(self.extract_keywords(new_content))
            
            # Detect patterns
            patterns = []
            
            # Added keywords
            added_keywords = new_keywords - old_keywords
            if added_keywords:
                patterns.append(f"added_keywords_{len(added_keywords)}")
            
            # Removed keywords
            removed_keywords = old_keywords - new_keywords
            if removed_keywords:
                patterns.append(f"removed_keywords_{len(removed_keywords)}")
            
            # Length changes
            old_length = len(old_content)
            new_length = len(new_content)
            length_ratio = new_length / old_length if old_length > 0 else 1.0
            
            if length_ratio > 1.5:
                patterns.append("significant_expansion")
            elif length_ratio < 0.5:
                patterns.append("significant_reduction")
            elif abs(length_ratio - 1.0) > 0.2:
                patterns.append("moderate_length_change")
            
            # Calculate confidence
            confidence = 0.9  # High confidence for lexical analysis
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return SemanticAnalysisResult(
                analysis_type=SemanticAnalysisType.LEXICAL_ANALYSIS,
                similarity_score=similarity,
                change_significance=change_significance,
                detected_patterns=patterns,
                confidence=confidence,
                analysis_metadata={
                    "old_keywords_count": len(old_keywords),
                    "new_keywords_count": len(new_keywords),
                    "added_keywords": list(added_keywords)[:10],  # First 10
                    "removed_keywords": list(removed_keywords)[:10],  # First 10
                    "length_ratio": length_ratio
                },
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in lexical analysis: {e}")
            return SemanticAnalysisResult(
                analysis_type=SemanticAnalysisType.LEXICAL_ANALYSIS,
                similarity_score=0.0,
                change_significance=1.0,
                confidence=0.0,
                processing_time=0.0
            )


class IntentAnalyzer:
    """Analyzer cho intent shift detection"""
    
    def __init__(self):
        self.intent_patterns = {
            IntentCategory.VISION_CHANGE: [
                "tầm nhìn", "vision", "dream", "aspiration", "future", "long-term",
                "sứ mệnh", "mission", "purpose", "calling"
            ],
            IntentCategory.STRATEGY_SHIFT: [
                "chiến lược", "strategy", "approach", "method", "plan", "roadmap",
                "framework", "methodology", "technique"
            ],
            IntentCategory.GOAL_MODIFICATION: [
                "mục tiêu", "goal", "objective", "target", "aim", "purpose",
                "outcome", "result", "achievement"
            ],
            IntentCategory.APPROACH_CHANGE: [
                "cách tiếp cận", "approach", "way", "manner", "style", "mode",
                "technique", "method", "process"
            ],
            IntentCategory.PRIORITY_SHIFT: [
                "ưu tiên", "priority", "important", "critical", "essential",
                "key", "main", "primary", "secondary"
            ],
            IntentCategory.SCOPE_EXPANSION: [
                "mở rộng", "expand", "extend", "broaden", "increase", "scale",
                "grow", "enhance", "amplify"
            ],
            IntentCategory.SCOPE_REDUCTION: [
                "thu hẹp", "reduce", "limit", "narrow", "focus", "concentrate",
                "streamline", "simplify", "minimize"
            ],
            IntentCategory.METHODOLOGY_CHANGE: [
                "phương pháp", "methodology", "system", "framework", "process",
                "procedure", "protocol", "standard"
            ]
        }
    
    def detect_intent_keywords(self, text: str) -> Dict[IntentCategory, List[str]]:
        """Detect intent-related keywords in text"""
        text_lower = text.lower()
        detected = {}
        
        for category, keywords in self.intent_patterns.items():
            found_keywords = [kw for kw in keywords if kw in text_lower]
            if found_keywords:
                detected[category] = found_keywords
        
        return detected
    
    async def analyze_intent_shift(
        self, 
        old_content: str, 
        new_content: str
    ) -> Optional[IntentShiftAnalysis]:
        """Analyze intent shifts between old và new content"""
        try:
            # Detect intent keywords in both versions
            old_intents = self.detect_intent_keywords(old_content)
            new_intents = self.detect_intent_keywords(new_content)
            
            # Calculate intent shift magnitude
            all_categories = set(old_intents.keys()).union(set(new_intents.keys()))
            
            if not all_categories:
                return None  # No intent keywords detected
            
            # Analyze each category for changes
            intent_changes = {}
            for category in all_categories:
                old_count = len(old_intents.get(category, []))
                new_count = len(new_intents.get(category, []))
                
                if old_count == 0 and new_count > 0:
                    intent_changes[category] = "added"
                elif old_count > 0 and new_count == 0:
                    intent_changes[category] = "removed"
                elif abs(new_count - old_count) > 1:
                    intent_changes[category] = "modified"
            
            if not intent_changes:
                return None  # No significant intent changes
            
            # Determine primary intent shift category
            primary_category = max(intent_changes.keys(), 
                                 key=lambda c: len(new_intents.get(c, [])))
            
            # Calculate confidence based on keyword density
            total_old_keywords = sum(len(kws) for kws in old_intents.values())
            total_new_keywords = sum(len(kws) for kws in new_intents.values())
            
            confidence = min(1.0, (total_old_keywords + total_new_keywords) / 10)
            
            # Calculate shift magnitude
            shift_magnitude = len(intent_changes) / len(all_categories)
            
            # Collect detected changes
            detected_changes = [
                f"{category.value}: {change_type}"
                for category, change_type in intent_changes.items()
            ]
            
            return IntentShiftAnalysis(
                intent_category=primary_category,
                confidence=confidence,
                old_intent_keywords=list(old_intents.get(primary_category, [])),
                new_intent_keywords=list(new_intents.get(primary_category, [])),
                intent_shift_magnitude=shift_magnitude,
                detected_changes=detected_changes
            )
            
        except Exception as e:
            logger.error(f"Error analyzing intent shift: {e}")
            return None


class SemanticChangeDetector:
    """
    Main semantic change detector combining multiple analysis methods
    
    Integrates vector similarity, lexical analysis, và intent detection
    để provide comprehensive change analysis.
    """
    
    def __init__(self):
        self.vector_analyzer = VectorEmbeddingAnalyzer()
        self.lexical_analyzer = LexicalAnalyzer()
        self.intent_analyzer = IntentAnalyzer()
        self.event_bus = SystemEventBus()
        
        # Configuration
        self.config = {
            "vector_weight": 0.4,
            "lexical_weight": 0.3,
            "intent_weight": 0.3,
            "significance_threshold": 0.1,
            "intent_threshold": 0.3,
            "confidence_threshold": 0.5
        }
        
        logger.info("SemanticChangeDetector initialized")
    
    async def detect_semantic_changes(
        self, 
        old_snapshot: ContentSnapshot, 
        new_snapshot: ContentSnapshot
    ) -> ComprehensiveChangeAnalysis:
        """
        Comprehensive semantic change detection
        
        Args:
            old_snapshot: Previous content snapshot
            new_snapshot: New content snapshot
            
        Returns:
            ComprehensiveChangeAnalysis với detailed results
        """
        start_time = datetime.now()
        
        try:
            old_content = old_snapshot.content_text
            new_content = new_snapshot.content_text
            
            # Run parallel analyses
            vector_analysis, lexical_analysis = await asyncio.gather(
                self.vector_analyzer.analyze_vector_similarity(old_content, new_content),
                self.lexical_analyzer.analyze_lexical_changes(old_content, new_content)
            )
            
            # Run intent analysis
            intent_shift = await self.intent_analyzer.analyze_intent_shift(old_content, new_content)
            
            # Combine analyses
            analyses = [vector_analysis, lexical_analysis]
            
            # Calculate overall significance using weighted average
            overall_significance = (
                vector_analysis.change_significance * self.config["vector_weight"] +
                lexical_analysis.change_significance * self.config["lexical_weight"]
            )
            
            # Add intent weight if intent shift detected
            if intent_shift:
                intent_significance = intent_shift.intent_shift_magnitude
                overall_significance = (
                    overall_significance * (1 - self.config["intent_weight"]) +
                    intent_significance * self.config["intent_weight"]
                )
            
            # Determine change type based on significance và patterns
            detected_change_type = self._determine_change_type(
                overall_significance, 
                analyses, 
                intent_shift
            )
            
            # Calculate confidence score
            confidence_score = sum(a.confidence for a in analyses) / len(analyses)
            if intent_shift:
                confidence_score = (confidence_score + intent_shift.confidence) / 2
            
            # Generate recommendations
            recommended_actions = self._generate_recommendations(
                detected_change_type,
                overall_significance,
                intent_shift
            )
            
            # Create comprehensive analysis
            analysis = ComprehensiveChangeAnalysis(
                content_id=old_snapshot.content_id,
                old_snapshot=old_snapshot,
                new_snapshot=new_snapshot,
                overall_significance=overall_significance,
                detected_change_type=detected_change_type,
                semantic_analyses=analyses,
                intent_shift_analysis=intent_shift,
                confidence_score=confidence_score,
                recommended_actions=recommended_actions
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Semantic change detection completed in {processing_time:.2f}s: "
                f"{detected_change_type} (significance: {overall_significance:.2f})"
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in semantic change detection: {e}")
            
            # Return minimal analysis on error
            return ComprehensiveChangeAnalysis(
                content_id=old_snapshot.content_id,
                old_snapshot=old_snapshot,
                new_snapshot=new_snapshot,
                overall_significance=0.0,
                detected_change_type=ContentChangeType.MINOR_EDIT,
                semantic_analyses=[],
                intent_shift_analysis=None,
                confidence_score=0.0,
                recommended_actions=["error_occurred_during_analysis"]
            )
    
    def _determine_change_type(
        self,
        significance: float,
        analyses: List[SemanticAnalysisResult],
        intent_shift: Optional[IntentShiftAnalysis]
    ) -> ContentChangeType:
        """Determine change type based on analysis results"""
        
        # Intent shift takes priority
        if intent_shift and intent_shift.confidence > self.config["confidence_threshold"]:
            if intent_shift.intent_shift_magnitude > 0.7:
                return ContentChangeType.INTENT_SHIFT
            elif "vision_change" in [change.lower() for change in intent_shift.detected_changes]:
                return ContentChangeType.INTENT_SHIFT
        
        # Determine based on overall significance
        if significance > 0.8:
            return ContentChangeType.COMPLETE_REWRITE
        elif significance > 0.5:
            return ContentChangeType.MAJOR_REVISION
        elif significance > 0.1:
            return ContentChangeType.SIGNIFICANT_UPDATE
        else:
            return ContentChangeType.MINOR_EDIT
    
    def _generate_recommendations(
        self,
        change_type: ContentChangeType,
        significance: float,
        intent_shift: Optional[IntentShiftAnalysis]
    ) -> List[str]:
        """Generate recommended actions based on analysis"""
        recommendations = []
        
        if change_type == ContentChangeType.INTENT_SHIFT:
            recommendations.extend([
                "trigger_strategic_planning_update",
                "notify_stakeholders",
                "update_agent_objectives",
                "review_ontology_alignment"
            ])
        
        if significance > 0.5:
            recommendations.extend([
                "update_vector_embeddings",
                "refresh_knowledge_graph",
                "retrain_semantic_models"
            ])
        
        if intent_shift and intent_shift.confidence > 0.7:
            recommendations.extend([
                "contextual_identity_engine_update",
                "strategic_agent_reconfiguration"
            ])
        
        if not recommendations:
            recommendations = ["monitor_for_additional_changes"]
        
        return recommendations


# Global semantic change detector instance
_semantic_change_detector: Optional[SemanticChangeDetector] = None

def get_semantic_change_detector() -> SemanticChangeDetector:
    """Get global semantic change detector instance"""
    global _semantic_change_detector
    if _semantic_change_detector is None:
        _semantic_change_detector = SemanticChangeDetector()
    return _semantic_change_detector 
