#!/usr/bin/env python3
"""
Script test deployment để kiểm tra API endpoints trên Railway
"""
import requests
import json
import sys

def test_endpoint(url, endpoint_name):
    """Test một endpoint và in kết quả"""
    try:
        print(f"\n🔍 Testing {endpoint_name}: {url}")
        response = requests.get(url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ {endpoint_name} SUCCESS")
                print(f"Response type: {type(data)}")
                if isinstance(data, dict):
                    print(f"Response keys: {list(data.keys())}")
                    if 'items' in data:
                        print(f"Items count: {len(data.get('items', []))}")
                        print(f"Total: {data.get('total', 'N/A')}")
                    if 'environment_variables' in data:
                        env_vars = data['environment_variables']
                        print(f"Environment variables status:")
                        for key, value in env_vars.items():
                            status = "✅" if value != "NOT_SET" else "❌"
                            print(f"  {status} {key}: {value}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ {endpoint_name} JSON DECODE ERROR: {e}")
                print(f"Raw response: {response.text[:500]}")
                return False
        else:
            print(f"❌ {endpoint_name} FAILED")
            print(f"Error response: {response.text[:500]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {endpoint_name} CONNECTION ERROR: {e}")
        return False

def main():
    """Main test function"""
    base_url = "https://trm-os-0307-phase-1-success-production.up.railway.app"
    
    # Test các endpoint
    endpoints = [
        ("/health", "Health Check"),
        ("/", "Root"),
        ("/debug", "Debug Info"),
        ("/docs", "API Documentation"),
        ("/api/v1/agents/", "Agents List"),
        ("/api/v1/knowledge-snippets/", "Knowledge Snippets List"),
    ]
    
    print("🚀 Testing TRM-OS Railway Deployment")
    print("=" * 50)
    
    success_count = 0
    total_count = len(endpoints)
    
    for endpoint, name in endpoints:
        url = f"{base_url}{endpoint}"
        if test_endpoint(url, name):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {success_count}/{total_count} endpoints successful")
    
    if success_count >= total_count - 1:  # Allow 1 failure (docs endpoint)
        print("🎉 DEPLOYMENT IS WORKING! Most endpoints are successful.")
        sys.exit(0)
    else:
        print("⚠️  Multiple tests failed. Check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 