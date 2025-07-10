"""
TRM-OS: Commercial AI Strategic Coordinator
Điều phối strategic insights từ multiple Commercial AI services
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    """Supported Commercial AI providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"

class StrategicInsightType(Enum):
    """Types of strategic insights"""
    OPPORTUNITY_ANALYSIS = "opportunity_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    MARKET_TRENDS = "market_trends"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    STRATEGIC_PLANNING = "strategic_planning"

@dataclass
class AIInsight:
    """Strategic insight từ AI provider"""
    insight_id: str
    provider: AIProvider
    insight_type: StrategicInsightType
    title: str
    content: str
    confidence_score: float
    supporting_data: Dict[str, Any]
    recommendations: List[str]
    risk_factors: List[str]
    opportunities: List[str]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategicSynthesis:
    """Synthesized strategic analysis từ multiple AI providers"""
    synthesis_id: str
    query: str
    participating_providers: List[AIProvider]
    individual_insights: List[AIInsight]
    synthesized_recommendations: List[str]
    consensus_areas: List[str]
    divergent_opinions: List[str]
    overall_confidence: float
    risk_assessment: Dict[str, Any]
    opportunity_assessment: Dict[str, Any]
    action_priorities: List[str]
    created_at: datetime

class CommercialAIStrategicCoordinator:
    """
    Điều phối strategic analysis từ multiple Commercial AI providers
    Tuân thủ AGE v2.0 philosophy: Multi-AI strategic intelligence coordination
    """
    
    def __init__(self):
        self.ai_clients = {}  # Will be populated với actual AI clients
        self.insight_history: List[AIInsight] = []
        self.synthesis_history: List[StrategicSynthesis] = []
        
        # Configuration
        self.min_consensus_threshold = 0.7
        self.max_providers_per_query = 3
        self.insight_retention_days = 90
        
        logger.info("CommercialAIStrategicCoordinator initialized với multi-AI coordination")

    async def get_strategic_insights(self,
                                   query: str,
                                   insight_type: StrategicInsightType,
                                   providers: Optional[List[AIProvider]] = None,
                                   context: Optional[Dict[str, Any]] = None) -> StrategicSynthesis:
        """
        Get strategic insights từ multiple AI providers và synthesize
        
        Args:
            query: Strategic question hoặc analysis request
            insight_type: Type of strategic insight needed
            providers: Specific providers to use (default: all available)
            context: Additional context cho analysis
            
        Returns:
            StrategicSynthesis với combined insights
        """
        try:
            # 1. Determine participating providers
            participating_providers = providers or [AIProvider.OPENAI, AIProvider.CLAUDE, AIProvider.GEMINI]
            
            # 2. Get insights từ each provider
            individual_insights = []
            tasks = []
            
            for provider in participating_providers:
                task = self._get_insight_from_provider(provider, query, insight_type, context)
                tasks.append(task)
            
            # Execute trong parallel
            provider_insights = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 3. Process results
            for i, insight_result in enumerate(provider_insights):
                if isinstance(insight_result, AIInsight):
                    individual_insights.append(insight_result)
                elif isinstance(insight_result, Exception):
                    logger.warning(f"Error từ {participating_providers[i]}: {insight_result}")
            
            if not individual_insights:
                raise ValueError("No insights obtained từ any provider")
            
            # 4. Synthesize insights
            synthesis = await self._synthesize_insights(query, individual_insights)
            
            # 5. Store results
            self.insight_history.extend(individual_insights)
            self.synthesis_history.append(synthesis)
            
            # 6. Cleanup old insights
            await self._cleanup_old_insights()
            
            logger.info(f"Strategic synthesis completed với {len(individual_insights)} insights")
            
            return synthesis
            
        except Exception as e:
            logger.error(f"Error getting strategic insights: {e}")
            raise

    async def _get_insight_from_provider(self,
                                       provider: AIProvider,
                                       query: str,
                                       insight_type: StrategicInsightType,
                                       context: Optional[Dict[str, Any]] = None) -> AIInsight:
        """Get insight từ specific AI provider"""
        try:
            # Mock implementation - trong production sẽ call actual AI APIs
            
            # Simulate AI provider response
            mock_insights = {
                AIProvider.OPENAI: {
                    "content": f"OpenAI analysis: {query} - Comprehensive strategic evaluation with data-driven insights",
                    "confidence": 0.85,
                    "recommendations": ["Implement data-driven approach", "Focus on scalable solutions", "Optimize resource allocation"],
                    "risks": ["Market volatility", "Implementation complexity"],
                    "opportunities": ["Emerging market segments", "Technology advancement"]
                },
                AIProvider.CLAUDE: {
                    "content": f"Claude analysis: {query} - Nuanced strategic perspective with risk-aware recommendations",
                    "confidence": 0.82,
                    "recommendations": ["Adopt cautious growth strategy", "Diversify risk portfolio", "Strengthen core capabilities"],
                    "risks": ["Regulatory changes", "Competitive pressure"],
                    "opportunities": ["Strategic partnerships", "Process innovation"]
                },
                AIProvider.GEMINI: {
                    "content": f"Gemini analysis: {query} - Multi-dimensional strategic assessment with innovation focus",
                    "confidence": 0.88,
                    "recommendations": ["Embrace innovative approaches", "Leverage emerging technologies", "Build adaptive capabilities"],
                    "risks": ["Technology disruption", "Resource constraints"],
                    "opportunities": ["Digital transformation", "Market expansion"]
                }
            }
            
            mock_data = mock_insights.get(provider, mock_insights[AIProvider.OPENAI])
            
            insight = AIInsight(
                insight_id=f"{provider.value}_{datetime.now().timestamp()}",
                provider=provider,
                insight_type=insight_type,
                title=f"Strategic Analysis: {insight_type.value.replace('_', ' ').title()}",
                content=mock_data["content"],
                confidence_score=mock_data["confidence"],
                supporting_data=context or {},
                recommendations=mock_data["recommendations"],
                risk_factors=mock_data["risks"],
                opportunities=mock_data["opportunities"],
                created_at=datetime.now(),
                metadata={
                    "query": query,
                    "provider_specific_data": f"{provider.value}_specific_metrics"
                }
            )
            
            # Simulate some processing delay
            await asyncio.sleep(0.1)
            
            return insight
            
        except Exception as e:
            logger.error(f"Error getting insight từ {provider}: {e}")
            raise

    async def _synthesize_insights(self,
                                 query: str,
                                 insights: List[AIInsight]) -> StrategicSynthesis:
        """Synthesize insights từ multiple providers"""
        try:
            # 1. Extract all recommendations
            all_recommendations = []
            for insight in insights:
                all_recommendations.extend(insight.recommendations)
            
            # 2. Find consensus recommendations
            recommendation_counts = {}
            for rec in all_recommendations:
                # Simple keyword-based clustering
                rec_key = rec.lower()
                recommendation_counts[rec_key] = recommendation_counts.get(rec_key, 0) + 1
            
            # Recommendations mentioned by multiple providers
            consensus_recommendations = [
                rec for rec, count in recommendation_counts.items() 
                if count >= max(2, len(insights) * self.min_consensus_threshold)
            ]
            
            # 3. Synthesize final recommendations
            synthesized_recommendations = list(set(all_recommendations))[:10]  # Top 10 unique recommendations
            
            # 4. Find consensus areas
            consensus_areas = []
            if len(consensus_recommendations) > 0:
                consensus_areas.append("Multiple AI providers agree on key strategic directions")
            
            # Check for risk consensus
            all_risks = []
            for insight in insights:
                all_risks.extend(insight.risk_factors)
            
            risk_counts = {}
            for risk in all_risks:
                risk_key = risk.lower()
                risk_counts[risk_key] = risk_counts.get(risk_key, 0) + 1
            
            consensus_risks = [risk for risk, count in risk_counts.items() if count >= 2]
            if consensus_risks:
                consensus_areas.append("Consistent risk identification across providers")
            
            # 5. Find divergent opinions
            divergent_opinions = []
            
            # Compare confidence scores
            confidence_scores = [insight.confidence_score for insight in insights]
            if max(confidence_scores) - min(confidence_scores) > 0.2:
                divergent_opinions.append("Significant confidence variation across providers")
            
            # Check for unique recommendations
            unique_recommendations = [
                rec for rec, count in recommendation_counts.items() 
                if count == 1
            ]
            if len(unique_recommendations) > len(consensus_recommendations):
                divergent_opinions.append("Providers offer diverse strategic perspectives")
            
            # 6. Calculate overall confidence
            overall_confidence = sum(confidence_scores) / len(confidence_scores)
            
            # 7. Risk assessment
            all_risk_factors = []
            for insight in insights:
                all_risk_factors.extend(insight.risk_factors)
            
            risk_assessment = {
                'identified_risks': list(set(all_risk_factors)),
                'consensus_risks': consensus_risks,
                'risk_coverage': len(set(all_risk_factors)),
                'risk_consensus_level': len(consensus_risks) / max(len(set(all_risk_factors)), 1)
            }
            
            # 8. Opportunity assessment
            all_opportunities = []
            for insight in insights:
                all_opportunities.extend(insight.opportunities)
            
            opportunity_counts = {}
            for opp in all_opportunities:
                opp_key = opp.lower()
                opportunity_counts[opp_key] = opportunity_counts.get(opp_key, 0) + 1
            
            consensus_opportunities = [opp for opp, count in opportunity_counts.items() if count >= 2]
            
            opportunity_assessment = {
                'identified_opportunities': list(set(all_opportunities)),
                'consensus_opportunities': consensus_opportunities,
                'opportunity_coverage': len(set(all_opportunities)),
                'opportunity_consensus_level': len(consensus_opportunities) / max(len(set(all_opportunities)), 1)
            }
            
            # 9. Action priorities
            action_priorities = []
            
            # High consensus recommendations = high priority
            if consensus_recommendations:
                action_priorities.extend(consensus_recommendations[:3])
            
            # Add highest confidence recommendations
            sorted_insights = sorted(insights, key=lambda x: x.confidence_score, reverse=True)
            if sorted_insights:
                top_recommendations = sorted_insights[0].recommendations[:2]
                action_priorities.extend(top_recommendations)
            
            # Remove duplicates và limit
            action_priorities = list(dict.fromkeys(action_priorities))[:5]
            
            synthesis = StrategicSynthesis(
                synthesis_id=f"synthesis_{datetime.now().timestamp()}",
                query=query,
                participating_providers=[insight.provider for insight in insights],
                individual_insights=insights,
                synthesized_recommendations=synthesized_recommendations,
                consensus_areas=consensus_areas,
                divergent_opinions=divergent_opinions,
                overall_confidence=overall_confidence,
                risk_assessment=risk_assessment,
                opportunity_assessment=opportunity_assessment,
                action_priorities=action_priorities,
                created_at=datetime.now()
            )
            
            return synthesis
            
        except Exception as e:
            logger.error(f"Error synthesizing insights: {e}")
            raise

    async def _cleanup_old_insights(self):
        """Cleanup old insights to manage memory"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.insight_retention_days)
            
            # Filter recent insights
            self.insight_history = [
                insight for insight in self.insight_history
                if insight.created_at >= cutoff_date
            ]
            
            # Filter recent syntheses
            self.synthesis_history = [
                synthesis for synthesis in self.synthesis_history
                if synthesis.created_at >= cutoff_date
            ]
            
            logger.info(f"Cleaned up insights older than {self.insight_retention_days} days")
            
        except Exception as e:
            logger.warning(f"Error cleaning up old insights: {e}")

    async def get_insight_history(self,
                                insight_type: Optional[StrategicInsightType] = None,
                                provider: Optional[AIProvider] = None,
                                days: int = 30) -> List[AIInsight]:
        """Get insight history với filtering"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            filtered_insights = []
            for insight in self.insight_history:
                if insight.created_at < cutoff_date:
                    continue
                
                if insight_type and insight.insight_type != insight_type:
                    continue
                
                if provider and insight.provider != provider:
                    continue
                
                filtered_insights.append(insight)
            
            return filtered_insights
            
        except Exception as e:
            logger.error(f"Error getting insight history: {e}")
            return []

    async def get_synthesis_history(self, days: int = 30) -> List[StrategicSynthesis]:
        """Get synthesis history"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            filtered_syntheses = [
                synthesis for synthesis in self.synthesis_history
                if synthesis.created_at >= cutoff_date
            ]
            
            return filtered_syntheses
            
        except Exception as e:
            logger.error(f"Error getting synthesis history: {e}")
            return []

    async def analyze_provider_performance(self) -> Dict[str, Any]:
        """Analyze performance của different AI providers"""
        try:
            if not self.insight_history:
                return {"message": "No insight history available"}
            
            provider_stats = {}
            
            for provider in AIProvider:
                provider_insights = [
                    insight for insight in self.insight_history
                    if insight.provider == provider
                ]
                
                if provider_insights:
                    avg_confidence = sum(i.confidence_score for i in provider_insights) / len(provider_insights)
                    avg_recommendations = sum(len(i.recommendations) for i in provider_insights) / len(provider_insights)
                    avg_risks = sum(len(i.risk_factors) for i in provider_insights) / len(provider_insights)
                    avg_opportunities = sum(len(i.opportunities) for i in provider_insights) / len(provider_insights)
                    
                    provider_stats[provider.value] = {
                        'total_insights': len(provider_insights),
                        'average_confidence': avg_confidence,
                        'average_recommendations_per_insight': avg_recommendations,
                        'average_risks_per_insight': avg_risks,
                        'average_opportunities_per_insight': avg_opportunities,
                        'insight_types_covered': len(set(i.insight_type for i in provider_insights))
                    }
                else:
                    provider_stats[provider.value] = {
                        'total_insights': 0,
                        'status': 'no_data'
                    }
            
            return provider_stats
            
        except Exception as e:
            logger.error(f"Error analyzing provider performance: {e}")
            return {"error": str(e)}

    async def get_consensus_metrics(self) -> Dict[str, Any]:
        """Get metrics về consensus across syntheses"""
        try:
            if not self.synthesis_history:
                return {"message": "No synthesis history available"}
            
            metrics = {
                'total_syntheses': len(self.synthesis_history),
                'average_consensus_areas': 0,
                'average_divergent_opinions': 0,
                'average_overall_confidence': 0,
                'consensus_trend': []
            }
            
            total_consensus = sum(len(s.consensus_areas) for s in self.synthesis_history)
            total_divergent = sum(len(s.divergent_opinions) for s in self.synthesis_history)
            total_confidence = sum(s.overall_confidence for s in self.synthesis_history)
            
            metrics['average_consensus_areas'] = total_consensus / len(self.synthesis_history)
            metrics['average_divergent_opinions'] = total_divergent / len(self.synthesis_history)
            metrics['average_overall_confidence'] = total_confidence / len(self.synthesis_history)
            
            # Consensus trend (last 10 syntheses)
            recent_syntheses = sorted(self.synthesis_history, key=lambda x: x.created_at)[-10:]
            for synthesis in recent_syntheses:
                metrics['consensus_trend'].append({
                    'date': synthesis.created_at.isoformat(),
                    'consensus_score': len(synthesis.consensus_areas) / max(len(synthesis.consensus_areas) + len(synthesis.divergent_opinions), 1),
                    'confidence': synthesis.overall_confidence
                })
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting consensus metrics: {e}")
            return {"error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            'total_insights': len(self.insight_history),
            'total_syntheses': len(self.synthesis_history),
            'supported_providers': [provider.value for provider in AIProvider],
            'supported_insight_types': [insight_type.value for insight_type in StrategicInsightType],
            'configuration': {
                'min_consensus_threshold': self.min_consensus_threshold,
                'max_providers_per_query': self.max_providers_per_query,
                'insight_retention_days': self.insight_retention_days
            },
            'recent_activity_30d': {
                'insights': len([i for i in self.insight_history if (datetime.now() - i.created_at).days <= 30]),
                'syntheses': len([s for s in self.synthesis_history if (datetime.now() - s.created_at).days <= 30])
            }
        } 