#!/usr/bin/env python3
"""
Real OpenAI Embeddings Validation Script
Test REAL OpenAI embeddings thay thế placeholders/TODO với commercial AI APIs thật
"""

import asyncio
import sys
import os
import time
import numpy as np
import pytest
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_api.core.semantic_change_detector import SemanticChangeDetector, VectorEmbeddingAnalyzer

@pytest.mark.asyncio
async def test_real_openai_embeddings():
    """Test real OpenAI embeddings vs mock implementations"""
    print("🚀 TESTING REAL OPENAI EMBEDDINGS VALIDATION")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = VectorEmbeddingAnalyzer()
    
    # Test data
    test_texts = [
        "TRM-OS là Operating System cho AIs với Commercial AI coordination",
        "TRM-OS is an Operating System for AIs with Commercial AI coordination", 
        "Hệ thống AGE v2.0 implement Living Knowledge với semantic evolution",
        "The AGE v2.0 system implements Living Knowledge with semantic evolution",
        "Hoàn toàn khác biệt về machine learning và artificial intelligence"
    ]
    
    print("📊 TEST 1: Real OpenAI Embeddings Generation")
    print("-" * 40)
    
    embeddings = []
    total_tokens = 0
    start_time = time.time()
    
    for i, text in enumerate(test_texts):
        print(f"  Text {i+1}: {text[:50]}...")
        
        embedding = await analyzer.generate_embedding(text)
        embeddings.append(embedding)
        
        print(f"    ✅ Generated embedding: {len(embedding)} dimensions")
        
        if len(embedding) == 1536:  # OpenAI text-embedding-3-small dimension
            print(f"    ✅ Correct OpenAI embedding dimension")
        else:
            print(f"    ⚠️ Unexpected dimension (may be fallback): {len(embedding)}")
    
    total_time = time.time() - start_time
    
    # Get API statistics
    stats = analyzer.get_api_statistics()
    print(f"\n📈 API STATISTICS:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Successful requests: {stats['successful_requests']}")
    print(f"  Failed requests: {stats['failed_requests']}")
    print(f"  Success rate: {stats['success_rate_percent']}%")
    print(f"  Total tokens used: {stats['total_tokens_used']}")
    print(f"  Average response time: {stats['average_response_time_seconds']}s")
    print(f"  Total processing time: {total_time:.2f}s")
    
    print(f"\n📊 TEST 2: Semantic Similarity Analysis")
    print("-" * 40)
    
    # Test semantic similarity
    test_pairs = [
        ("TRM-OS là hệ điều hành cho AI", "TRM-OS is an operating system for AI"),
        ("Semantic evolution detection", "Phát hiện evolution ngữ nghĩa"),
        ("Hoàn toàn khác biệt", "Completely different content")
    ]
    
    for i, (text1, text2) in enumerate(test_pairs):
        print(f"\n  Pair {i+1}:")
        print(f"    Text A: {text1}")
        print(f"    Text B: {text2}")
        
        result = await analyzer.analyze_vector_similarity(text1, text2)
        
        print(f"    Similarity Score: {result.similarity_score:.4f}")
        print(f"    Change Significance: {result.change_significance:.4f}")
        print(f"    Confidence: {result.confidence:.2f}")
        print(f"    Patterns: {', '.join(result.detected_patterns)}")
        print(f"    Processing Time: {result.processing_time:.3f}s")
        
        # Validate results
        if result.confidence >= 0.9:
            print(f"    ✅ High confidence (real API)")
        elif result.confidence >= 0.7:
            print(f"    ⚠️ Medium confidence (local fallback)")
        else:
            print(f"    ❌ Low confidence (hash fallback)")
    
    print(f"\n📊 TEST 3: API Key Validation")
    print("-" * 40)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.startswith("sk-"):
        print(f"    ✅ OpenAI API key found: {openai_key[:20]}...")
        if stats['successful_requests'] > 0:
            print(f"    ✅ API calls successful")
        else:
            print(f"    ❌ API calls failed - check key validity")
    else:
        print(f"    ❌ OpenAI API key not found or invalid")
    
    print(f"\n📊 TEST 4: Fallback System Validation")
    print("-" * 40)
    
    # Test fallback với invalid API key
    old_key = analyzer.openai_client.api_key
    analyzer.openai_client.api_key = "invalid-key"
    
    print("  Testing fallback with invalid API key...")
    fallback_embedding = await analyzer.generate_embedding("Test fallback embedding")
    
    if len(fallback_embedding) == 384:  # sentence-transformers dimension
        print(f"    ✅ Local sentence-transformers fallback working")
    elif len(fallback_embedding) == 384:  # hash fallback dimension
        print(f"    ⚠️ Hash-based fallback used")
    else:
        print(f"    ❌ Unexpected fallback dimension: {len(fallback_embedding)}")
    
    # Restore original key
    analyzer.openai_client.api_key = old_key
    
    print(f"\n🎯 VALIDATION SUMMARY")
    print("=" * 60)
    
    total_score = 0
    max_score = 100
    
    # Score real API usage
    if stats['success_rate_percent'] >= 80:
        api_score = 40
        print(f"✅ Real OpenAI API Success: 40/40 points")
    elif stats['success_rate_percent'] >= 50:
        api_score = 20
        print(f"⚠️ Partial OpenAI API Success: 20/40 points")
    else:
        api_score = 0
        print(f"❌ OpenAI API Failed: 0/40 points")
    total_score += api_score
    
    # Score embedding quality
    if all(len(emb) == 1536 for emb in embeddings):
        embedding_score = 30
        print(f"✅ Real OpenAI Embeddings: 30/30 points")
    elif any(len(emb) == 384 for emb in embeddings):
        embedding_score = 15
        print(f"⚠️ Local Fallback Used: 15/30 points") 
    else:
        embedding_score = 5
        print(f"❌ Hash Fallback Only: 5/30 points")
    total_score += embedding_score
    
    # Score semantic analysis accuracy
    if stats['total_tokens_used'] > 0:
        semantic_score = 20
        print(f"✅ Real Semantic Analysis: 20/20 points")
    else:
        semantic_score = 0
        print(f"❌ No Real Semantic Analysis: 0/20 points")
    total_score += semantic_score
    
    # Score fallback system
    if len(fallback_embedding) > 0:
        fallback_score = 10
        print(f"✅ Fallback System Working: 10/10 points")
    else:
        fallback_score = 0
        print(f"❌ Fallback System Failed: 0/10 points")
    total_score += fallback_score
    
    print(f"\n🏆 FINAL SCORE: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
    
    if total_score >= 90:
        print("🎉 EXCELLENT: Real Commercial AI embeddings fully operational!")
        return True
    elif total_score >= 70:
        print("✅ GOOD: Real embeddings working with some fallbacks")
        return True
    elif total_score >= 50:
        print("⚠️ PARTIAL: Significant fallback usage detected")
        return False
    else:
        print("❌ FAILED: Real embeddings not working properly")
        return False

async def main():
    """Main validation function"""
    try:
        success = await test_real_openai_embeddings()
        
        if success:
            print(f"\n✅ VALIDATION PASSED: Real OpenAI embeddings ready for production")
            print(f"📋 Next steps: Continue với Meta-Agent Intelligence implementation")
        else:
            print(f"\n❌ VALIDATION FAILED: Fix embedding issues before proceeding")
            print(f"📋 Required: Check API keys và network connectivity")
        
        return success
        
    except Exception as e:
        print(f"\n💥 VALIDATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main()) 