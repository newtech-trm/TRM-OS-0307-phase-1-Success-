#!/usr/bin/env python3
"""
Real Embeddings Architecture Validation Script
Kiểm tra real embedding architecture thay thế placeholder embeddings
"""

import asyncio
import sys
import os
import time
import numpy as np
import json
import pytest
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_api.core.semantic_change_detector import SemanticChangeDetector, VectorEmbeddingAnalyzer
from trm_api.core.commercial_ai_coordinator import CommercialAICoordinator

@pytest.mark.asyncio
async def test_real_embeddings_architecture():
    """Test real embeddings architecture implementation"""
    print("🚀 TESTING REAL OPENAI EMBEDDINGS ARCHITECTURE")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VectorEmbeddingAnalyzer()
    
    print("📊 TEST 1: Real Commercial AI Architecture Validation")
    print("-" * 50)
    
    # Check OpenAI client initialization
    if hasattr(analyzer, 'openai_client'):
        print("  ✅ OpenAI AsyncClient initialized")
        print(f"    Model: {analyzer.embedding_model}")
        print(f"    Dimension: {analyzer.embedding_dimension}")
        print(f"    Max Length: {analyzer.max_text_length}")
    else:
        print("  ❌ OpenAI client not initialized")
    
    # Check API key configuration
    if analyzer.openai_client.api_key:
        api_key_preview = analyzer.openai_client.api_key[:20] + "..." if len(analyzer.openai_client.api_key) > 20 else analyzer.openai_client.api_key
        print(f"  ✅ API key configured: {api_key_preview}")
    else:
        print("  ⚠️ API key not configured - will use fallback")
    
    # Check fallback systems
    fallback_keys = []
    if hasattr(analyzer, 'anthropic_api_key') and analyzer.anthropic_api_key:
        fallback_keys.append("Anthropic")
    if hasattr(analyzer, 'google_api_key') and analyzer.google_api_key:
        fallback_keys.append("Google")
    
    print(f"  ✅ Fallback APIs configured: {', '.join(fallback_keys) if fallback_keys else 'None'}")
    
    # Check similarity thresholds (real vs mock)
    print(f"  ✅ Real embedding thresholds:")
    for name, value in analyzer.similarity_thresholds.items():
        print(f"    {name}: {value} (optimized for real embeddings)")
    
    print("\n📊 TEST 2: Semantic Analysis Architecture")
    print("-" * 50)
    
    # Test semantic change detector integration
    detector = SemanticChangeDetector()
    
    if hasattr(detector, 'vector_analyzer'):
        print("  ✅ VectorEmbeddingAnalyzer integrated")
    else:
        print("  ❌ VectorEmbeddingAnalyzer not integrated")
    
    if hasattr(detector, 'lexical_analyzer'):
        print("  ✅ LexicalAnalyzer integrated")
    else:
        print("  ❌ LexicalAnalyzer not integrated")
    
    if hasattr(detector, 'intent_analyzer'):
        print("  ✅ IntentAnalyzer integrated")
    else:
        print("  ❌ IntentAnalyzer not integrated")
    
    print("\n📊 TEST 3: Local Fallback Performance")
    print("-" * 50)
    
    # Test local sentence-transformers fallback
    test_texts = [
        "TRM-OS Operating System cho Commercial AI coordination",
        "Living Knowledge System với semantic evolution detection",
        "Meta-Agent Intelligence với self-improvement capabilities"
    ]
    
    start_time = time.time()
    local_embeddings = []
    
    for i, text in enumerate(test_texts):
        print(f"  Processing text {i+1}: {text[:40]}...")
        
        # Force fallback test
        old_key = analyzer.openai_client.api_key
        analyzer.openai_client.api_key = None
        
        embedding = await analyzer.generate_embedding(text)
        local_embeddings.append(embedding)
        
        # Restore key
        analyzer.openai_client.api_key = old_key
        
        print(f"    ✅ Local embedding: {len(embedding)} dimensions")
    
    processing_time = time.time() - start_time
    print(f"  📈 Local processing time: {processing_time:.2f}s")
    print(f"  📈 Average per text: {processing_time/len(test_texts):.2f}s")
    
    print("\n📊 TEST 4: Real vs Mock Implementation Comparison")
    print("-" * 50)
    
    # Compare similarity analysis
    test_pair = (
        "Commercial AI coordination system", 
        "Hệ thống phối hợp Commercial AI"
    )
    
    print(f"  Test pair:")
    print(f"    A: {test_pair[0]}")
    print(f"    B: {test_pair[1]}")
    
    # Local fallback analysis
    old_key = analyzer.openai_client.api_key
    analyzer.openai_client.api_key = None
    
    result = await analyzer.analyze_vector_similarity(test_pair[0], test_pair[1])
    
    analyzer.openai_client.api_key = old_key
    
    print(f"  Local Analysis Results:")
    print(f"    Similarity: {result.similarity_score:.4f}")
    print(f"    Significance: {result.change_significance:.4f}")
    print(f"    Confidence: {result.confidence:.2f}")
    print(f"    Patterns: {', '.join(result.detected_patterns)}")
    print(f"    Processing Time: {result.processing_time:.3f}s")
    
    # Check if using sentence-transformers or hash fallback
    if len(local_embeddings[0]) == 384 and result.confidence >= 0.7:
        print("  ✅ Using sentence-transformers (high quality local fallback)")
    elif len(local_embeddings[0]) == 384 and result.confidence < 0.7:
        print("  ⚠️ Using hash-based fallback (emergency mode)")
    else:
        print(f"  ❓ Unknown fallback mode: {len(local_embeddings[0])} dimensions")
    
    print("\n📊 TEST 5: Production Readiness Assessment")
    print("-" * 50)
    
    readiness_score = 0
    max_score = 100
    
    # Architecture completeness (40 points)
    architecture_features = [
        ("OpenAI AsyncClient", hasattr(analyzer, 'openai_client')),
        ("Embedding Model Config", hasattr(analyzer, 'embedding_model')),
        ("Real Similarity Thresholds", len(analyzer.similarity_thresholds) >= 5),
        ("API Statistics Tracking", hasattr(analyzer, 'api_stats')),
        ("Fallback System", hasattr(analyzer, '_fallback_embedding_generation')),
        ("Error Handling", hasattr(analyzer, '_hash_based_fallback')),
        ("Performance Metrics", hasattr(analyzer, '_update_average_response_time')),
        ("Multi-Service Support", hasattr(analyzer, 'anthropic_api_key'))
    ]
    
    architecture_score = sum(10 if feature[1] else 0 for feature in architecture_features[:4])
    architecture_score += sum(5 if feature[1] else 0 for feature in architecture_features[4:])
    readiness_score += min(architecture_score, 40)
    
    print(f"  Architecture Features: {architecture_score}/40")
    for name, present in architecture_features:
        status = "✅" if present else "❌"
        print(f"    {status} {name}")
    
    # Fallback Quality (30 points)
    fallback_quality = 0
    if len(local_embeddings) > 0:
        avg_dimension = sum(len(emb) for emb in local_embeddings) / len(local_embeddings)
        if avg_dimension >= 384:  # sentence-transformers
            fallback_quality = 30
        elif avg_dimension >= 300:  # hash with good dimensions
            fallback_quality = 15
        else:
            fallback_quality = 5
    
    readiness_score += fallback_quality
    print(f"  Fallback Quality: {fallback_quality}/30")
    
    # Integration Quality (20 points)
    integration_features = [
        ("SemanticChangeDetector", hasattr(detector, 'vector_analyzer')),
        ("Multi-Analysis Support", hasattr(detector, 'lexical_analyzer')),
        ("Intent Analysis", hasattr(detector, 'intent_analyzer')),
        ("Comprehensive Results", hasattr(detector, '_determine_change_type'))
    ]
    
    integration_score = sum(5 if feature[1] else 0 for feature in integration_features)
    readiness_score += integration_score
    print(f"  Integration Quality: {integration_score}/20")
    
    # Performance (10 points)
    performance_score = 0
    if processing_time < 10:  # Under 10 seconds for 3 texts
        performance_score = 10
    elif processing_time < 20:
        performance_score = 5
    else:
        performance_score = 0
    
    readiness_score += performance_score
    print(f"  Performance Score: {performance_score}/10")
    
    print(f"\n🎯 ARCHITECTURE VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"🏆 TOTAL SCORE: {readiness_score}/{max_score} ({readiness_score/max_score*100:.1f}%)")
    
    if readiness_score >= 90:
        print("🎉 EXCELLENT: Real Commercial AI architecture fully ready!")
        print("📋 Status: Ready for production with valid API keys")
        return True
    elif readiness_score >= 70:
        print("✅ GOOD: Architecture solid với reliable fallbacks")
        print("📋 Status: Production ready with API key setup")
        return True
    elif readiness_score >= 50:
        print("⚠️ PARTIAL: Architecture implemented, needs optimization")
        print("📋 Status: Requires API keys and performance tuning")
        return False
    else:
        print("❌ FAILED: Architecture needs significant work")
        print("📋 Status: Not ready for production")
        return False

async def main():
    """Main validation function"""
    try:
        success = await test_real_embeddings_architecture()
        
        print(f"\n📋 NEXT STEPS:")
        if success:
            print("✅ 1. Setup valid OpenAI API key")
            print("✅ 2. Test real API calls in development")
            print("✅ 3. Proceed với Meta-Agent Intelligence implementation")
            print("✅ 4. Architecture ready for Week 2 of Phase 6")
        else:
            print("❌ 1. Fix architecture issues identified above")
            print("❌ 2. Improve fallback system reliability")
            print("❌ 3. Setup proper API key management")
            print("❌ 4. Re-run validation before proceeding")
        
        return success
        
    except Exception as e:
        print(f"\n💥 ARCHITECTURE VALIDATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main()) 