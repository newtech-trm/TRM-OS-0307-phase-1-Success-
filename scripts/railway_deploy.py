#!/usr/bin/env python
# coding: utf-8

"""
RAILWAY DEPLOYMENT AUTOMATION SCRIPT cho TRM-OS v1.0
====================================================

Script hỗ trợ deployment và monitoring cho Railway platform.
Tự động hóa các tác vụ deployment và verification.

Features:
- Pre-deployment verification
- Health check monitoring
- Database seeding
- Post-deployment testing
- Error reporting và rollback support

Usage:
    python scripts/railway_deploy.py --action deploy
    python scripts/railway_deploy.py --action verify
    python scripts/railway_deploy.py --action seed
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('railway_deployment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RailwayDeploymentManager:
    """Railway deployment automation và monitoring"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('RAILWAY_APP_URL', 'https://your-app-url.railway.app')
        self.api_base = f"{self.base_url}/api/v1"
        self.timeout = 30
        self.max_retries = 3
        
    def verify_prerequisites(self) -> bool:
        """Verify deployment prerequisites"""
        logger.info("🔍 Verifying deployment prerequisites...")
        
        checks = {
            "Git Repository": self._check_git_status(),
            "Docker Build": self._check_docker_build(),
            "Environment Variables": self._check_env_vars(),
            "Dependencies": self._check_dependencies()
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    def _check_git_status(self) -> bool:
        """Check git repository status"""
        try:
            import subprocess
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                 capture_output=True, text=True, timeout=10)
            return result.returncode == 0 and len(result.stdout.strip()) == 0
        except Exception as e:
            logger.error(f"Git check failed: {e}")
            return False
    
    def _check_docker_build(self) -> bool:
        """Check if Docker build would succeed"""
        try:
            import subprocess
            result = subprocess.run(['docker', 'build', '-t', 'trm-os-test', '.'], 
                                 capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Docker build check failed: {e}")
            return False
    
    def _check_env_vars(self) -> bool:
        """Check required environment variables"""
        required_vars = [
            'NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD',
            'SECRET_KEY', 'PROJECT_NAME'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing environment variables: {missing_vars}")
            return False
        
        return True
    
    def _check_dependencies(self) -> bool:
        """Check if all dependencies are properly installed"""
        try:
            import subprocess
            result = subprocess.run(['pip', 'check'], 
                                 capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Dependencies check failed: {e}")
            return False
    
    def wait_for_deployment(self, max_wait_minutes: int = 10) -> bool:
        """Wait for deployment to complete"""
        logger.info(f"⏳ Waiting for deployment to complete (max {max_wait_minutes} minutes)...")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while time.time() - start_time < max_wait_seconds:
            try:
                response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
                if response.status_code == 200:
                    logger.info("✅ Deployment completed successfully!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(30)  # Check every 30 seconds
            logger.info("⏳ Still waiting for deployment...")
        
        logger.error("❌ Deployment timeout!")
        return False
    
    def verify_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        logger.info("🏥 Running comprehensive health checks...")
        
        health_results = {
            "basic_health": self._check_basic_health(),
            "api_health": self._check_api_health(),
            "database_health": self._check_database_health(),
            "endpoints_health": self._check_endpoints_health()
        }
        
        overall_health = all(health_results.values())
        
        logger.info(f"🏥 Overall health: {'✅ HEALTHY' if overall_health else '❌ UNHEALTHY'}")
        
        return {
            "overall_healthy": overall_health,
            "details": health_results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_basic_health(self) -> bool:
        """Basic application health check"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Basic health check failed: {e}")
            return False
    
    def _check_api_health(self) -> bool:
        """API health check"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            return False
    
    def _check_database_health(self) -> bool:
        """Database connectivity check"""
        try:
            response = requests.get(f"{self.api_base}/admin/db-health", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def _check_endpoints_health(self) -> bool:
        """Check critical API endpoints"""
        critical_endpoints = [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/api/v1/agents",
            "/api/v1/projects"
        ]
        
        failed_endpoints = []
        for endpoint in critical_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
                if response.status_code not in [200, 401]:  # 401 is OK for protected endpoints
                    failed_endpoints.append(endpoint)
            except Exception:
                failed_endpoints.append(endpoint)
        
        if failed_endpoints:
            logger.error(f"Failed endpoints: {failed_endpoints}")
            return False
        
        return True
    
    def seed_database(self) -> bool:
        """Seed production database"""
        logger.info("🌱 Seeding production database...")
        
        try:
            # Use the unified seed script
            response = requests.post(
                f"{self.api_base}/admin/seed-database",
                json={"environment": "production", "force": False},
                timeout=120  # Seeding can take longer
            )
            
            if response.status_code == 200:
                logger.info("✅ Database seeded successfully!")
                return True
            else:
                logger.error(f"❌ Database seeding failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Database seeding error: {e}")
            return False
    
    def run_post_deployment_tests(self) -> bool:
        """Run post-deployment verification tests"""
        logger.info("🧪 Running post-deployment tests...")
        
        test_results = {
            "api_endpoints": self._test_api_endpoints(),
            "data_integrity": self._test_data_integrity(),
            "performance": self._test_performance()
        }
        
        all_passed = all(test_results.values())
        
        for test_name, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"{status} {test_name}")
        
        return all_passed
    
    def _test_api_endpoints(self) -> bool:
        """Test critical API endpoints"""
        try:
            # Test agents endpoint
            response = requests.get(f"{self.api_base}/agents", timeout=self.timeout)
            if response.status_code not in [200, 401]:
                return False
            
            # Test projects endpoint
            response = requests.get(f"{self.api_base}/projects", timeout=self.timeout)
            if response.status_code not in [200, 401]:
                return False
            
            return True
        except Exception as e:
            logger.error(f"API endpoints test failed: {e}")
            return False
    
    def _test_data_integrity(self) -> bool:
        """Test basic data integrity"""
        try:
            # This would typically test database connections and basic queries
            response = requests.get(f"{self.api_base}/admin/db-health", timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Data integrity test failed: {e}")
            return False
    
    def _test_performance(self) -> bool:
        """Test basic performance metrics"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_base}/health", timeout=self.timeout)
            response_time = time.time() - start_time
            
            # Should respond within 2 seconds
            if response.status_code == 200 and response_time < 2.0:
                logger.info(f"⚡ Response time: {response_time:.2f}s")
                return True
            else:
                logger.error(f"❌ Slow response: {response_time:.2f}s")
                return False
                
        except Exception as e:
            logger.error(f"Performance test failed: {e}")
            return False
    
    def generate_deployment_report(self, health_results: Dict[str, Any], 
                                 test_results: bool) -> str:
        """Generate comprehensive deployment report"""
        report = f"""
# TRM-OS Railway Deployment Report
Generated: {datetime.utcnow().isoformat()}

## 🚀 Deployment Summary
- **Application URL**: {self.base_url}
- **API Base**: {self.api_base}
- **Overall Health**: {'✅ HEALTHY' if health_results['overall_healthy'] else '❌ UNHEALTHY'}
- **Tests Passed**: {'✅ ALL PASSED' if test_results else '❌ SOME FAILED'}

## 🏥 Health Check Results
- **Basic Health**: {'✅' if health_results['details']['basic_health'] else '❌'}
- **API Health**: {'✅' if health_results['details']['api_health'] else '❌'}
- **Database Health**: {'✅' if health_results['details']['database_health'] else '❌'}
- **Endpoints Health**: {'✅' if health_results['details']['endpoints_health'] else '❌'}

## 📊 Key URLs
- **Application**: {self.base_url}
- **API Documentation**: {self.base_url}/docs
- **ReDoc**: {self.base_url}/redoc
- **Health Check**: {self.base_url}/health

## 🎯 Next Steps
1. Monitor application performance
2. Set up alerts and monitoring
3. Configure domain/SSL if needed
4. Schedule regular health checks

## 🔗 Railway Dashboard
https://railway.com/project/6c79655c-bde0-4772-b630-a63581e750ca?environmentId=64d3b32e-8a88-49ba-ad24-f6fc6c988a95

**Status**: {'🟢 PRODUCTION READY' if health_results['overall_healthy'] and test_results else '🔴 NEEDS ATTENTION'}
"""
        return report


def main():
    """Main deployment automation function"""
    parser = argparse.ArgumentParser(description='TRM-OS Railway Deployment Automation')
    parser.add_argument('--action', choices=['verify', 'deploy', 'seed', 'test', 'full'], 
                       default='full', help='Action to perform')
    parser.add_argument('--url', help='Railway application URL')
    
    args = parser.parse_args()
    
    # Initialize deployment manager
    manager = RailwayDeploymentManager(args.url)
    
    logger.info("🚀 TRM-OS Railway Deployment Automation Started")
    logger.info(f"📋 Action: {args.action}")
    logger.info(f"🌐 URL: {manager.base_url}")
    
    if args.action in ['verify', 'full']:
        logger.info("=" * 50)
        logger.info("🔍 VERIFICATION PHASE")
        logger.info("=" * 50)
        
        if not manager.verify_prerequisites():
            logger.error("❌ Prerequisites verification failed!")
            sys.exit(1)
    
    if args.action in ['deploy', 'full']:
        logger.info("=" * 50)
        logger.info("🚀 DEPLOYMENT PHASE")
        logger.info("=" * 50)
        
        if not manager.wait_for_deployment():
            logger.error("❌ Deployment failed!")
            sys.exit(1)
    
    if args.action in ['seed', 'full']:
        logger.info("=" * 50)
        logger.info("🌱 DATABASE SEEDING PHASE")
        logger.info("=" * 50)
        
        if not manager.seed_database():
            logger.error("❌ Database seeding failed!")
            sys.exit(1)
    
    if args.action in ['test', 'full']:
        logger.info("=" * 50)
        logger.info("🧪 TESTING PHASE")
        logger.info("=" * 50)
        
        # Health checks
        health_results = manager.verify_health()
        
        # Post-deployment tests
        test_results = manager.run_post_deployment_tests()
        
        # Generate report
        report = manager.generate_deployment_report(health_results, test_results)
        
        # Save report
        with open('railway_deployment_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("📋 Deployment report saved to: railway_deployment_report.md")
        
        if health_results['overall_healthy'] and test_results:
            logger.info("🎉 DEPLOYMENT SUCCESSFUL!")
            logger.info("🟢 TRM-OS v1.0 is LIVE and HEALTHY on Railway!")
        else:
            logger.error("❌ DEPLOYMENT NEEDS ATTENTION!")
            sys.exit(1)
    
    logger.info("✅ Railway deployment automation completed!")


if __name__ == "__main__":
    main() 