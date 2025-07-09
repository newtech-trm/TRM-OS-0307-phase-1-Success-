#!/usr/bin/env python3

import requests
import json

BASE_URL = "https://trmosngonlanh.up.railway.app"

# Test các endpoints theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md
endpoints_to_test = [
    "/",
    "/health", 
    "/api/v1/projects/",
    "/api/v1/agents/",
    "/api/v1/events/",
    "/api/v1/tensions/",
    "/api/v1/wins/",
    "/api/v1/tasks/",
    "/api/v1/recognitions/",
    "/api/v1/commercial-ai/",
    "/api/v1/reasoning/",
    "/api/v2/conversations/",
    "/api/v2/health"
]

print("🔍 TESTING TRM-OS API ENDPOINTS")
print("=" * 50)

for endpoint in endpoints_to_test:
    try:
        url = BASE_URL + endpoint
        response = requests.get(url, timeout=10)
        
        status_emoji = "✅" if response.status_code == 200 else "❌" if response.status_code == 404 else "⚠️"
        print(f"{status_emoji} {endpoint} -> {response.status_code}")
        
        if response.status_code == 200 and endpoint in ["/", "/health"]:
            try:
                data = response.json()
                print(f"   📄 Response: {json.dumps(data, indent=2)[:100]}...")
            except:
                print(f"   📄 Response: {response.text[:100]}...")
                
    except Exception as e:
        print(f"🚨 {endpoint} -> ERROR: {str(e)}")

print("\n🎯 GAPS ANALYSIS:")
print("=" * 50)

# Kiểm tra endpoints theo AGE_COMPREHENSIVE_SYSTEM_DESIGN_V2.md
required_by_age = [
    "Strategic Feedback Loop endpoints",
    "Self-Healing System endpoints", 
    "Evolution Pathway endpoints",
    "Temporal Reasoning endpoints",
    "AGE Orchestration endpoints",
    "Commercial AI Coordination endpoints",
    "Quantum WIN States endpoints"
]

for requirement in required_by_age:
    print(f"❌ MISSING: {requirement}") 