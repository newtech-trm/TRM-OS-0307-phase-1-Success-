#!/usr/bin/env python
# coding: utf-8

"""
TRM-OS Deployment Readiness Checker
==================================

Script kiểm tra tất cả các yêu cầu cho Railway deployment
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class DeploymentChecker:
    """Kiểm tra deployment readiness"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.checks = []
        self.errors = []
        self.warnings = []
        
    def check_file_exists(self, file_path: str, required: bool = True) -> bool:
        """Kiểm tra file có tồn tại không"""
        full_path = self.project_root / file_path
        exists = full_path.exists()
        
        if exists:
            self.checks.append(f"✅ {file_path} exists")
        else:
            message = f"❌ {file_path} missing"
            if required:
                self.errors.append(message)
            else:
                self.warnings.append(message)
                
        return exists
    
    def check_python_imports(self) -> bool:
        """Kiểm tra Python imports"""
        try:
            import trm_api.main
            self.checks.append("✅ TRM-API imports successfully")
            return True
        except ImportError as e:
            self.errors.append(f"❌ Python import failed: {e}")
            return False
    
    def check_railway_cli(self) -> bool:
        """Kiểm tra Railway CLI"""
        try:
            result = subprocess.run(['railway', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.checks.append(f"✅ Railway CLI installed: {version}")
                return True
            else:
                self.errors.append("❌ Railway CLI not working")
                return False
        except FileNotFoundError:
            self.errors.append("❌ Railway CLI not installed")
            return False
    
    def check_railway_config(self) -> bool:
        """Kiểm tra Railway configuration files"""
        config_files = [
            'railway.json',
            'nixpacks.toml', 
            'Procfile',
            'railway.env'
        ]
        
        all_exist = True
        for file in config_files:
            if not self.check_file_exists(file):
                all_exist = False
                
        return all_exist
    
    def check_requirements(self) -> bool:
        """Kiểm tra requirements.txt"""
        if not self.check_file_exists('requirements.txt'):
            return False
            
        try:
            with open(self.project_root / 'requirements.txt', 'r') as f:
                requirements = f.read()
                
            essential_packages = [
                'fastapi', 'uvicorn', 'neomodel', 'neo4j',
                'pydantic', 'python-dotenv'
            ]
            
            missing = []
            for package in essential_packages:
                if package not in requirements.lower():
                    missing.append(package)
            
            if missing:
                self.warnings.append(f"⚠️ Missing packages in requirements.txt: {', '.join(missing)}")
            else:
                self.checks.append("✅ All essential packages in requirements.txt")
                
            return len(missing) == 0
            
        except Exception as e:
            self.errors.append(f"❌ Error reading requirements.txt: {e}")
            return False
    
    def check_environment_variables(self) -> bool:
        """Kiểm tra environment variables"""
        env_file = self.project_root / '.env'
        railway_env = self.project_root / 'railway.env'
        
        if not env_file.exists() and not railway_env.exists():
            self.warnings.append("⚠️ No environment file found")
            return False
            
        self.checks.append("✅ Environment configuration available")
        return True
    
    def check_documentation(self) -> bool:
        """Kiểm tra documentation"""
        docs = [
            'README.md',
            'RAILWAY_DEPLOYMENT_GUIDE.md',
            'DEPLOYMENT_CHECKLIST.md',
            'docs/API_V1_COMPREHENSIVE_GUIDE.md'
        ]
        
        all_exist = True
        for doc in docs:
            if not self.check_file_exists(doc):
                all_exist = False
                
        return all_exist
    
    def check_git_status(self) -> bool:
        """Kiểm tra git status"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout.strip():
                    self.warnings.append("⚠️ Uncommitted changes in git")
                    return False
                else:
                    self.checks.append("✅ Git working tree clean")
                    return True
            else:
                self.warnings.append("⚠️ Git status check failed")
                return False
        except FileNotFoundError:
            self.warnings.append("⚠️ Git not available")
            return False
    
    def run_all_checks(self) -> Dict:
        """Chạy tất cả checks"""
        print("🔍 Checking TRM-OS Railway Deployment Readiness...")
        print("=" * 60)
        
        # Core application checks
        print("\n📦 Application Checks:")
        self.check_python_imports()
        self.check_requirements()
        self.check_environment_variables()
        
        # Railway specific checks
        print("\n🚀 Railway Checks:")
        self.check_railway_cli()
        self.check_railway_config()
        
        # Documentation checks
        print("\n📚 Documentation Checks:")
        self.check_documentation()
        
        # Git checks
        print("\n🔄 Git Checks:")
        self.check_git_status()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DEPLOYMENT READINESS SUMMARY")
        print("=" * 60)
        
        # Print results
        if self.checks:
            print(f"\n✅ PASSED ({len(self.checks)} checks):")
            for check in self.checks:
                print(f"  {check}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)} items):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)} items):")
            for error in self.errors:
                print(f"  {error}")
        
        # Final verdict
        print("\n" + "=" * 60)
        if self.errors:
            print("❌ DEPLOYMENT NOT READY - Fix errors first!")
            readiness_score = 0
        elif self.warnings:
            print("⚠️  DEPLOYMENT READY WITH WARNINGS - Proceed with caution")
            readiness_score = 75
        else:
            print("✅ DEPLOYMENT FULLY READY - All checks passed!")
            readiness_score = 100
        
        print(f"📊 Readiness Score: {readiness_score}%")
        
        return {
            'ready': len(self.errors) == 0,
            'score': readiness_score,
            'checks_passed': len(self.checks),
            'warnings': len(self.warnings),
            'errors': len(self.errors),
            'details': {
                'checks': self.checks,
                'warnings': self.warnings,
                'errors': self.errors
            }
        }

def main():
    """Main function"""
    checker = DeploymentChecker()
    result = checker.run_all_checks()
    
    # Exit with appropriate code
    if result['ready']:
        print("\n🎉 Ready for Railway deployment!")
        sys.exit(0)
    else:
        print("\n🛠️  Fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main() 