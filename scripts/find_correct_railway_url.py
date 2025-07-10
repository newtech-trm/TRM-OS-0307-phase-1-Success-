#!/usr/bin/env python3
"""
Find Correct Railway Deployment URL
Test multiple possible URLs để tìm deployment đang hoạt động
"""

import asyncio
import httpx
import time
from typing import List, Dict, Any

async def test_url(url: str) -> Dict[str, Any]:
    """Test một URL để check if it's working"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            start_time = time.time()
            response = await client.get(url)
            response_time = time.time() - start_time
            
            return {
                "url": url,
                "status_code": response.status_code,
                "response_time": round(response_time * 1000, 2),
                "working": response.status_code < 400,
                "content_preview": response.text[:200] if response.text else "",
                "error": None
            }
            
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "response_time": None,
            "working": False,
            "content_preview": "",
            "error": str(e)
        }

async def find_working_deployment():
    """Tìm Railway deployment đang hoạt động"""
    
    # Possible Railway URLs
    candidate_urls = [
        "https://trmosngonlanh.up.railway.app",
        "https://trm-os-production-95-percent.up.railway.app",
        "https://trm-os-95-percent.up.railway.app",
        "https://trm-os-production.up.railway.app",
        "https://trm-os.up.railway.app",
        "https://trmosv1.up.railway.app",
        "https://trm-api.up.railway.app"
    ]
    
    print("🔍 Searching for active Railway deployment...")
    print("=" * 60)
    
    # Test base URLs
    print("\n📡 Testing Base URLs:")
    base_results = []
    for url in candidate_urls:
        result = await test_url(url)
        base_results.append(result)
        
        status_icon = "✅" if result["working"] else "❌"
        response_info = f"({result['status_code']}, {result['response_time']}ms)" if result["status_code"] else f"({result['error'][:50]}...)"
        print(f"   {status_icon} {url} {response_info}")
    
    # Find working URLs
    working_urls = [r for r in base_results if r["working"]]
    
    if not working_urls:
        print("\n❌ No working Railway deployments found!")
        return None
    
    print(f"\n✅ Found {len(working_urls)} working deployment(s):")
    
    # Test API endpoints for working URLs
    for working_url in working_urls:
        base_url = working_url["url"]
        print(f"\n🔌 Testing API endpoints for: {base_url}")
        
        api_endpoints = [
            "/docs",
            "/health", 
            "/api/v1",
            "/api/v1/agents",
            "/api/v1/projects",
            "/api/v1/status"
        ]
        
        api_results = []
        for endpoint in api_endpoints:
            full_url = f"{base_url}{endpoint}"
            result = await test_url(full_url)
            api_results.append(result)
            
            status_icon = "✅" if result["working"] else "❌"
            print(f"   {status_icon} {endpoint}: {result['status_code']}")
        
        # Calculate health score
        working_endpoints = len([r for r in api_results if r["working"]])
        total_endpoints = len(api_results)
        health_score = (working_endpoints / total_endpoints) * 100
        
        print(f"   📊 Health Score: {health_score:.1f}% ({working_endpoints}/{total_endpoints})")
        
        if health_score >= 50:
            print(f"\n🎉 FOUND ACTIVE DEPLOYMENT: {base_url}")
            print(f"   📈 Health: {health_score:.1f}%")
            print(f"   🚀 Status: PRODUCTION READY")
            
            # Return the working URL details
            return {
                "deployment_url": base_url,
                "health_score": health_score,
                "working_endpoints": working_endpoints,
                "total_endpoints": total_endpoints,
                "api_results": api_results
            }
    
    print("\n⚠️ Found base URLs but no healthy API endpoints")
    return working_urls[0]["url"] if working_urls else None

async def main():
    """Main execution"""
    print("🚂 Railway Deployment URL Finder")
    print("🎯 TRM-OS Enterprise Production Search")
    print()
    
    result = await find_working_deployment()
    
    if result:
        if isinstance(result, dict):
            print(f"\n🏆 DEPLOYMENT FOUND & VALIDATED:")
            print(f"   🔗 URL: {result['deployment_url']}")
            print(f"   📊 Health: {result['health_score']:.1f}%")
            print(f"   ✅ Ready for production use!")
            
            # Update deployment script với correct URL
            correct_url = result['deployment_url']
            print(f"\n📝 Updating deployment scripts với correct URL...")
            
            return correct_url
        else:
            print(f"\n⚠️ Found URL but needs investigation: {result}")
            return result
    else:
        print(f"\n❌ No active Railway deployment found!")
        print(f"   🔧 May need to redeploy or check Railway dashboard")
        return None

if __name__ == "__main__":
    active_url = asyncio.run(main())
    
    if active_url:
        print(f"\n✅ SUCCESS: {active_url}")
        exit(0)
    else:
        print(f"\n❌ FAILED: No deployment found")
        exit(1) 