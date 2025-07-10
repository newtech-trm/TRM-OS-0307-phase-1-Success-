#!/usr/bin/env python3
"""
Commercial AI Coordinator - TRM-OS v2.0

Central coordinator cho all commercial AI API calls:
- OpenAI GPT-4, Claude-3.5, Gemini Pro integration
- Intelligent routing và fallback systems
- Cost optimization và performance tracking
- Real embeddings, reasoning, và analysis

Philosophy: Unified commercial AI access với intelligent coordination
"""

import asyncio
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import openai
from openai import AsyncOpenAI
import anthropic
import google.generativeai as genai

from trm_api.core.logging_config import get_logger

logger = get_logger(__name__)


class AIProvider(str, Enum):
    """Commercial AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AUTO = "auto"


class TaskType(str, Enum):
    """Types of AI tasks"""
    EMBEDDING = "embedding"
    REASONING = "reasoning"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    TRANSLATION = "translation"


@dataclass
class AIRequest:
    """Request cho commercial AI services"""
    task_type: TaskType
    content: str
    context: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    preferred_provider: AIProvider = AIProvider.AUTO
    max_tokens: Optional[int] = None
    temperature: float = 0.7


@dataclass  
class AIResponse:
    """Response từ commercial AI services"""
    content: str
    provider_used: AIProvider
    model_used: str
    tokens_used: int
    cost_estimate: float
    processing_time: float
    confidence_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderStats:
    """Statistics cho AI provider"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    success_rate: float = 0.0


class CommercialAICoordinator:
    """Central coordinator cho all commercial AI services"""
    
    def __init__(self):
        self.logger = get_logger("commercial_ai_coordinator")
        
        # Initialize clients
        self.openai_client = None
        self.anthropic_client = None
        self.google_client = None
        
        # Provider configurations
        self.provider_configs = {
            AIProvider.OPENAI: {
                "models": {
                    TaskType.EMBEDDING: "text-embedding-3-small",
                    TaskType.REASONING: "gpt-4o",
                    TaskType.ANALYSIS: "gpt-4o",
                    TaskType.OPTIMIZATION: "gpt-4o",
                    TaskType.GENERATION: "gpt-4o"
                },
                "costs_per_1k_tokens": {
                    "text-embedding-3-small": 0.00002,
                    "gpt-4o": 0.03
                }
            },
            AIProvider.ANTHROPIC: {
                "models": {
                    TaskType.REASONING: "claude-3-5-sonnet-20241022",
                    TaskType.ANALYSIS: "claude-3-5-sonnet-20241022",
                    TaskType.OPTIMIZATION: "claude-3-5-sonnet-20241022",
                    TaskType.GENERATION: "claude-3-5-sonnet-20241022"
                },
                "costs_per_1k_tokens": {
                    "claude-3-5-sonnet-20241022": 0.025
                }
            },
            AIProvider.GOOGLE: {
                "models": {
                    TaskType.REASONING: "gemini-1.5-pro",
                    TaskType.ANALYSIS: "gemini-1.5-pro", 
                    TaskType.OPTIMIZATION: "gemini-1.5-pro",
                    TaskType.GENERATION: "gemini-1.5-pro"
                },
                "costs_per_1k_tokens": {
                    "gemini-1.5-pro": 0.020
                }
            }
        }
        
        # Provider statistics
        self.provider_stats = {
            provider: ProviderStats() 
            for provider in [AIProvider.OPENAI, AIProvider.ANTHROPIC, AIProvider.GOOGLE]
        }
        
        # Routing preferences (based on performance và cost)
        self.routing_preferences = {
            TaskType.EMBEDDING: AIProvider.OPENAI,      # Best embeddings
            TaskType.REASONING: AIProvider.ANTHROPIC,   # Best reasoning
            TaskType.ANALYSIS: AIProvider.OPENAI,       # Good analysis
            TaskType.OPTIMIZATION: AIProvider.ANTHROPIC, # Complex optimization
            TaskType.CLASSIFICATION: AIProvider.OPENAI,  # Fast classification
            TaskType.GENERATION: AIProvider.GOOGLE,     # Creative generation
            TaskType.TRANSLATION: AIProvider.GOOGLE     # Good translation
        }
        
        # Performance tracking
        self.performance_history: List[Dict[str, Any]] = []
        
    async def initialize(self) -> bool:
        """Initialize all commercial AI clients"""
        try:
            self.logger.info("Initializing Commercial AI Coordinator...")
            
            # Initialize OpenAI
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                self.openai_client = AsyncOpenAI(api_key=openai_key)
                self.logger.info("OpenAI client initialized")
            else:
                self.logger.warning("OpenAI API key not found")
            
            # Initialize Anthropic
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if anthropic_key:
                self.anthropic_client = anthropic.AsyncAnthropic(api_key=anthropic_key)
                self.logger.info("Anthropic client initialized")
            else:
                self.logger.warning("Anthropic API key not found")
            
            # Initialize Google
            google_key = os.getenv("GOOGLE_API_KEY")
            if google_key:
                genai.configure(api_key=google_key)
                self.google_client = genai.GenerativeModel('gemini-1.5-pro')
                self.logger.info("Google AI client initialized")
            else:
                self.logger.warning("Google API key not found")
            
            # Test connections
            await self._test_connections()
            
            self.logger.info("Commercial AI Coordinator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Commercial AI Coordinator: {e}")
            return False
    
    async def _test_connections(self) -> None:
        """Test all AI provider connections"""
        # Test OpenAI
        if self.openai_client:
            try:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                self.logger.info("OpenAI connection test successful")
            except Exception as e:
                self.logger.warning(f"OpenAI connection test failed: {e}")
        
        # Test Anthropic
        if self.anthropic_client:
            try:
                response = await self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Test"}]
                )
                self.logger.info("Anthropic connection test successful")
            except Exception as e:
                self.logger.warning(f"Anthropic connection test failed: {e}")
        
        # Test Google
        if self.google_client:
            try:
                response = self.google_client.generate_content("Test")
                self.logger.info("Google AI connection test successful")
            except Exception as e:
                self.logger.warning(f"Google AI connection test failed: {e}")
    
    async def process_request(self, request: AIRequest) -> AIResponse:
        """Process AI request với intelligent routing"""
        start_time = time.time()
        
        try:
            # Determine optimal provider
            provider = self._select_provider(request)
            
            # Route to appropriate provider
            if provider == AIProvider.OPENAI:
                response = await self._process_openai_request(request)
            elif provider == AIProvider.ANTHROPIC:
                response = await self._process_anthropic_request(request)
            elif provider == AIProvider.GOOGLE:
                response = await self._process_google_request(request)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_provider_stats(provider, True, processing_time, response.tokens_used, response.cost_estimate)
            
            # Track performance
            self.performance_history.append({
                "timestamp": datetime.now(),
                "task_type": request.task_type.value,
                "provider": provider.value,
                "processing_time": processing_time,
                "tokens_used": response.tokens_used,
                "cost": response.cost_estimate,
                "confidence": response.confidence_score
            })
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            provider = request.preferred_provider if request.preferred_provider != AIProvider.AUTO else self.routing_preferences.get(request.task_type, AIProvider.OPENAI)
            self._update_provider_stats(provider, False, processing_time, 0, 0.0)
            
            self.logger.error(f"AI request failed: {e}")
            
            # Try fallback if original failed
            if request.preferred_provider == AIProvider.AUTO:
                return await self._try_fallback_providers(request, [provider])
            else:
                raise
    
    def _select_provider(self, request: AIRequest) -> AIProvider:
        """Select optimal provider based on task type và performance"""
        if request.preferred_provider != AIProvider.AUTO:
            return request.preferred_provider
        
        # Use routing preferences with performance adjustment
        preferred = self.routing_preferences.get(request.task_type, AIProvider.OPENAI)
        
        # Check provider availability và performance
        preferred_stats = self.provider_stats[preferred]
        if preferred_stats.success_rate < 0.8 and preferred_stats.total_requests > 10:
            # Find better alternative
            alternatives = [p for p in AIProvider if p != preferred and p != AIProvider.AUTO]
            best_alternative = max(alternatives, key=lambda p: self.provider_stats[p].success_rate)
            return best_alternative
        
        return preferred
    
    async def _process_openai_request(self, request: AIRequest) -> AIResponse:
        """Process request using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        model = self.provider_configs[AIProvider.OPENAI]["models"].get(request.task_type, "gpt-4o")
        
        if request.task_type == TaskType.EMBEDDING:
            # Handle embeddings
            response = await self.openai_client.embeddings.create(
                model=model,
                input=request.content
            )
            
            embedding = response.data[0].embedding
            tokens_used = response.usage.total_tokens
            cost = self._calculate_cost(AIProvider.OPENAI, model, tokens_used)
            
            return AIResponse(
                content=json.dumps(embedding),
                provider_used=AIProvider.OPENAI,
                model_used=model,
                tokens_used=tokens_used,
                cost_estimate=cost,
                processing_time=0.0,  # Will be set by caller
                confidence_score=0.95,
                metadata={"embedding_dimension": len(embedding)}
            )
        
        else:
            # Handle text generation tasks
            messages = [{"role": "user", "content": request.content}]
            if request.context:
                messages.insert(0, {"role": "system", "content": request.context})
            
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=request.max_tokens or 1000,
                temperature=request.temperature
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = self._calculate_cost(AIProvider.OPENAI, model, tokens_used)
            
            return AIResponse(
                content=content,
                provider_used=AIProvider.OPENAI,
                model_used=model,
                tokens_used=tokens_used,
                cost_estimate=cost,
                processing_time=0.0,
                confidence_score=0.90,
                metadata={"finish_reason": response.choices[0].finish_reason}
            )
    
    async def _process_anthropic_request(self, request: AIRequest) -> AIResponse:
        """Process request using Anthropic Claude"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        model = self.provider_configs[AIProvider.ANTHROPIC]["models"].get(request.task_type, "claude-3-5-sonnet-20241022")
        
        messages = [{"role": "user", "content": request.content}]
        system_prompt = request.context if request.context else None
        
        response = await self.anthropic_client.messages.create(
            model=model,
            messages=messages,
            system=system_prompt,
            max_tokens=request.max_tokens or 1000
        )
        
        content = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        cost = self._calculate_cost(AIProvider.ANTHROPIC, model, tokens_used)
        
        return AIResponse(
            content=content,
            provider_used=AIProvider.ANTHROPIC,
            model_used=model,
            tokens_used=tokens_used,
            cost_estimate=cost,
            processing_time=0.0,
            confidence_score=0.92,
            metadata={"stop_reason": response.stop_reason}
        )
    
    async def _process_google_request(self, request: AIRequest) -> AIResponse:
        """Process request using Google Gemini"""
        if not self.google_client:
            raise ValueError("Google client not initialized")
        
        model = self.provider_configs[AIProvider.GOOGLE]["models"].get(request.task_type, "gemini-1.5-pro")
        
        # Prepare content với context
        full_content = request.content
        if request.context:
            full_content = f"Context: {request.context}\n\nRequest: {request.content}"
        
        response = self.google_client.generate_content(
            full_content,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request.max_tokens or 1000,
                temperature=request.temperature
            )
        )
        
        content = response.text
        # Estimate tokens (Google doesn't always provide exact count)
        tokens_used = len(content.split()) * 1.3  # Rough estimate
        cost = self._calculate_cost(AIProvider.GOOGLE, model, int(tokens_used))
        
        return AIResponse(
            content=content,
            provider_used=AIProvider.GOOGLE,
            model_used=model,
            tokens_used=int(tokens_used),
            cost_estimate=cost,
            processing_time=0.0,
            confidence_score=0.88,
            metadata={"safety_ratings": str(response.prompt_feedback)}
        )
    
    def _calculate_cost(self, provider: AIProvider, model: str, tokens: int) -> float:
        """Calculate cost estimate for API call"""
        try:
            cost_per_1k = self.provider_configs[provider]["costs_per_1k_tokens"].get(model, 0.02)
            return (tokens / 1000) * cost_per_1k
        except Exception:
            return 0.0
    
    async def _try_fallback_providers(self, request: AIRequest, failed_providers: List[AIProvider]) -> AIResponse:
        """Try fallback providers if primary fails"""
        available_providers = [p for p in [AIProvider.OPENAI, AIProvider.ANTHROPIC, AIProvider.GOOGLE] 
                             if p not in failed_providers]
        
        for provider in available_providers:
            try:
                fallback_request = AIRequest(
                    task_type=request.task_type,
                    content=request.content,
                    context=request.context,
                    parameters=request.parameters,
                    preferred_provider=provider,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature
                )
                
                if provider == AIProvider.OPENAI:
                    return await self._process_openai_request(fallback_request)
                elif provider == AIProvider.ANTHROPIC:
                    return await self._process_anthropic_request(fallback_request)
                elif provider == AIProvider.GOOGLE:
                    return await self._process_google_request(fallback_request)
                    
            except Exception as e:
                self.logger.warning(f"Fallback provider {provider} also failed: {e}")
                continue
        
        raise Exception("All AI providers failed")
    
    def _update_provider_stats(self, provider: AIProvider, success: bool, 
                              processing_time: float, tokens: int, cost: float) -> None:
        """Update provider statistics"""
        stats = self.provider_stats[provider]
        
        stats.total_requests += 1
        if success:
            stats.successful_requests += 1
            stats.total_tokens += tokens
            stats.total_cost += cost
        else:
            stats.failed_requests += 1
        
        # Update success rate
        stats.success_rate = stats.successful_requests / stats.total_requests
        
        # Update average response time
        if stats.successful_requests > 0:
            stats.average_response_time = (
                (stats.average_response_time * (stats.successful_requests - 1) + processing_time) 
                / stats.successful_requests
            )
    
    # Specialized methods cho different use cases
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings specifically"""
        request = AIRequest(
            task_type=TaskType.EMBEDDING,
            content=text,
            preferred_provider=AIProvider.OPENAI  # Best for embeddings
        )
        
        response = await self.process_request(request)
        return json.loads(response.content)
    
    async def perform_reasoning(self, query: str, context: str = None, 
                               reasoning_type: str = "analytical") -> str:
        """Perform structured reasoning"""
        reasoning_context = f"""You are an expert reasoning assistant. 
        Perform {reasoning_type} reasoning on the given query.
        Provide clear, step-by-step reasoning leading to a conclusion."""
        
        if context:
            reasoning_context += f"\n\nAdditional context: {context}"
        
        request = AIRequest(
            task_type=TaskType.REASONING,
            content=query,
            context=reasoning_context,
            preferred_provider=AIProvider.ANTHROPIC  # Best for reasoning
        )
        
        response = await self.process_request(request)
        return response.content
    
    async def analyze_data(self, data: str, analysis_type: str = "comprehensive") -> str:
        """Perform data analysis"""
        analysis_context = f"""You are an expert data analyst.
        Perform {analysis_type} analysis on the provided data.
        Identify patterns, insights, and recommendations."""
        
        request = AIRequest(
            task_type=TaskType.ANALYSIS,
            content=data,
            context=analysis_context,
            preferred_provider=AIProvider.OPENAI  # Good for analysis
        )
        
        response = await self.process_request(request)
        return response.content
    
    async def optimize_parameters(self, current_params: str, objectives: str) -> str:
        """Optimize parameters based on objectives"""
        optimization_context = f"""You are an expert optimization consultant.
        Analyze the current parameters and suggest optimizations to achieve the given objectives.
        Provide specific, actionable recommendations với quantified improvements."""
        
        content = f"Current parameters: {current_params}\n\nObjectives: {objectives}"
        
        request = AIRequest(
            task_type=TaskType.OPTIMIZATION,
            content=content,
            context=optimization_context,
            preferred_provider=AIProvider.ANTHROPIC  # Best for complex optimization
        )
        
        response = await self.process_request(request)
        return response.content
    
    def get_coordinator_stats(self) -> Dict[str, Any]:
        """Get comprehensive coordinator statistics"""
        return {
            "provider_stats": {
                provider.value: {
                    "total_requests": stats.total_requests,
                    "success_rate": stats.success_rate,
                    "total_tokens": stats.total_tokens,
                    "total_cost": stats.total_cost,
                    "avg_response_time": stats.average_response_time
                }
                for provider, stats in self.provider_stats.items()
            },
            "routing_preferences": {
                task.value: provider.value 
                for task, provider in self.routing_preferences.items()
            },
            "total_requests": sum(stats.total_requests for stats in self.provider_stats.values()),
            "total_cost": sum(stats.total_cost for stats in self.provider_stats.values()),
            "recent_performance": self.performance_history[-10:] if self.performance_history else []
        }


# Global coordinator instance
_coordinator_instance: Optional[CommercialAICoordinator] = None

async def get_commercial_ai_coordinator() -> CommercialAICoordinator:
    """Get global Commercial AI Coordinator instance"""
    global _coordinator_instance
    
    if _coordinator_instance is None:
        _coordinator_instance = CommercialAICoordinator()
        await _coordinator_instance.initialize()
    
    return _coordinator_instance 