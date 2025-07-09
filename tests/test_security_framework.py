"""
Test suite cho TRM-OS Phase 3 Security Framework

Test các security capabilities:
- Authentication system
- Authorization engine  
- JWT token management
- RBAC permissions
- Security policies
"""

import asyncio
import pytest
from datetime import datetime, timedelta
import secrets

from trm_api.security.authentication import (
    AuthenticationManager, UserCredentials, AuthResult
)
from trm_api.security.authorization import (
    AuthorizationEngine, AccessRequest, ResourceType, ActionType
)


async def test_security_framework():
    """Test comprehensive security framework"""
    print("🔒 Testing TRM-OS Phase 3 Security Framework")
    print("=" * 80)
    
    results = {
        'authentication': False,
        'authorization': False,
        'jwt_tokens': False,
        'rbac_permissions': False,
        'security_policies': False
    }
    
    # Test 1: Authentication System
    print("\n🔐 Testing Authentication System...")
    try:
        auth_manager = AuthenticationManager()
        
        # Test user registration
        credentials = UserCredentials(
            email="test@example.com",
            username="testuser",
            password="SecurePass123!"
        )
        
        register_result = await auth_manager.register_user(credentials)
        
        if register_result.success:
            print("   ✅ User registration successful")
            
            # Test authentication
            auth_result = await auth_manager.authenticate_user(
                credentials, 
                ip_address="192.168.1.100",
                user_agent="Test Agent"
            )
            
            if auth_result.success and auth_result.access_token:
                print("   ✅ User authentication successful")
                print(f"   📊 Session ID: {auth_result.session_id}")
                print(f"   📊 Token expires: {auth_result.expires_at}")
                
                # Test session verification
                session = await auth_manager.verify_session(auth_result.session_id)
                if session and session.is_active:
                    print("   ✅ Session verification successful")
                    results['authentication'] = True
                else:
                    print("   ❌ Session verification failed")
            else:
                print("   ❌ User authentication failed")
        else:
            print(f"   ❌ User registration failed: {register_result.error_message}")
        
        if results['authentication']:
            print("✅ Authentication System: PASSED")
        else:
            print("❌ Authentication System: FAILED")
            
    except Exception as e:
        print(f"❌ Authentication System: FAILED - {e}")
    
    # Test 2: Authorization Engine
    print("\n🛡️ Testing Authorization Engine...")
    try:
        auth_engine = AuthorizationEngine()
        
        # Create test user và assign role
        user_id = "test_user_auth"
        auth_engine.rbac_manager.assign_role_to_user(user_id, "user")
        
        # Test authorization request
        access_request = AccessRequest(
            user_id=user_id,
            resource_type=ResourceType.PROJECT,
            action=ActionType.READ,
            resource_id="project_123",
            context={"hour": 14}  # Business hours
        )
        
        auth_result = await auth_engine.authorize(access_request)
        
        if auth_result.granted:
            print("   ✅ Access authorization successful")
            print(f"   📊 Matched permissions: {auth_result.matched_permissions}")
            print(f"   📊 Reason: {auth_result.reason}")
            
            # Test unauthorized access
            admin_request = AccessRequest(
                user_id=user_id,
                resource_type=ResourceType.SYSTEM,
                action=ActionType.ADMIN,
                context={"hour": 14}
            )
            
            admin_result = await auth_engine.authorize(admin_request)
            
            if not admin_result.granted:
                print("   ✅ Unauthorized access properly denied")
                results['authorization'] = True
            else:
                print("   ❌ Unauthorized access incorrectly granted")
        else:
            print(f"   ❌ Access authorization failed: {auth_result.reason}")
        
        if results['authorization']:
            print("✅ Authorization Engine: PASSED")
        else:
            print("❌ Authorization Engine: FAILED")
            
    except Exception as e:
        print(f"❌ Authorization Engine: FAILED - {e}")
    
    # Test 3: JWT Token Management
    print("\n🎫 Testing JWT Token Management...")
    try:
        auth_manager = AuthenticationManager()
        jwt_manager = auth_manager.jwt_manager
        
        # Create tokens
        user_id = "test_jwt_user"
        permissions = ["project.read", "task.create"]
        
        access_token = jwt_manager.create_access_token(user_id, permissions)
        refresh_token = jwt_manager.create_refresh_token(user_id)
        
        print("   ✅ JWT tokens created successfully")
        
        # Verify access token
        access_payload = jwt_manager.verify_token(access_token)
        if access_payload and access_payload.get('sub') == user_id:
            print("   ✅ Access token verification successful")
            print(f"   📊 Token permissions: {access_payload.get('permissions', [])}")
            
            # Test token refresh
            new_access_token = jwt_manager.refresh_access_token(refresh_token)
            if new_access_token:
                print("   ✅ Token refresh successful")
                results['jwt_tokens'] = True
            else:
                print("   ❌ Token refresh failed")
        else:
            print("   ❌ Access token verification failed")
        
        if results['jwt_tokens']:
            print("✅ JWT Token Management: PASSED")
        else:
            print("❌ JWT Token Management: FAILED")
            
    except Exception as e:
        print(f"❌ JWT Token Management: FAILED - {e}")
    
    # Test 4: RBAC Permissions
    print("\n👥 Testing RBAC Permissions...")
    try:
        auth_engine = AuthorizationEngine()
        rbac_manager = auth_engine.rbac_manager
        
        # Test role assignment
        test_user = "rbac_test_user"
        rbac_manager.assign_role_to_user(test_user, "manager")
        
        # Test permission checking
        has_project_read = rbac_manager.has_permission(
            test_user, ResourceType.PROJECT, ActionType.READ
        )
        has_system_admin = rbac_manager.has_permission(
            test_user, ResourceType.SYSTEM, ActionType.ADMIN
        )
        
        if has_project_read and not has_system_admin:
            print("   ✅ RBAC permission checking works correctly")
            
            # Test user permissions summary
            permissions_summary = auth_engine.get_user_permissions_summary(test_user)
            print(f"   📊 User roles: {permissions_summary['roles']}")
            print(f"   📊 Permissions count: {permissions_summary['permissions_count']}")
            
            results['rbac_permissions'] = True
        else:
            print("   ❌ RBAC permission checking failed")
        
        if results['rbac_permissions']:
            print("✅ RBAC Permissions: PASSED")
        else:
            print("❌ RBAC Permissions: FAILED")
            
    except Exception as e:
        print(f"❌ RBAC Permissions: FAILED - {e}")
    
    # Test 5: Security Policies
    print("\n📋 Testing Security Policies...")
    try:
        auth_engine = AuthorizationEngine()
        policy_engine = auth_engine.policy_engine
        
        # Test policy evaluation
        business_hours_context = {
            "hour": 14,  # 2 PM - within business hours
            "user_id": "policy_test_user"
        }
        
        after_hours_context = {
            "hour": 22,  # 10 PM - after business hours
            "user_id": "policy_test_user"
        }
        
        # Test business hours policy
        business_hours_ok = policy_engine.evaluate_policy("business_hours", business_hours_context)
        after_hours_blocked = not policy_engine.evaluate_policy("business_hours", after_hours_context)
        
        if business_hours_ok and after_hours_blocked:
            print("   ✅ Business hours policy working correctly")
            
            # Test policy with authorization
            auth_engine.rbac_manager.assign_role_to_user("policy_test_user", "user")
            
            # During business hours - should be allowed
            business_request = AccessRequest(
                user_id="policy_test_user",
                resource_type=ResourceType.PROJECT,
                action=ActionType.READ,
                context=business_hours_context
            )
            
            business_result = await auth_engine.authorize(business_request)
            
            # After hours - should be denied
            after_hours_request = AccessRequest(
                user_id="policy_test_user",
                resource_type=ResourceType.PROJECT,
                action=ActionType.READ,
                context=after_hours_context
            )
            
            after_hours_result = await auth_engine.authorize(after_hours_request)
            
            if business_result.granted and not after_hours_result.granted:
                print("   ✅ Policy-based authorization working correctly")
                results['security_policies'] = True
            else:
                print("   ❌ Policy-based authorization failed")
        else:
            print("   ❌ Business hours policy failed")
        
        if results['security_policies']:
            print("✅ Security Policies: PASSED")
        else:
            print("❌ Security Policies: FAILED")
            
    except Exception as e:
        print(f"❌ Security Policies: FAILED - {e}")
    
    # Final Results
    print(f"\n{'='*80}")
    print("📊 SECURITY FRAMEWORK TEST RESULTS")
    print(f"{'='*80}")
    
    passed_tests = sum(results.values())
    total_tests = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\n📈 Overall Score: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🎉 SECURITY FRAMEWORK: PERFECT!")
        print("🔒 Enterprise-grade security ready for production")
    elif passed_tests >= 4:
        print("🎉 SECURITY FRAMEWORK: EXCELLENT!")
        print("🔒 Strong security capabilities operational")
    elif passed_tests >= 3:
        print("✅ SECURITY FRAMEWORK: GOOD!")
        print("🔧 Minor security improvements needed")
    else:
        print("⚠️ SECURITY FRAMEWORK: NEEDS IMPROVEMENT")
        print("🛠️ Significant security work required")
    
    return results


async def test_password_security():
    """Test password security features"""
    print("\n🔑 Testing Password Security...")
    
    try:
        auth_manager = AuthenticationManager()
        password_manager = auth_manager.password_manager
        
        # Test password strength validation
        weak_password = "123"
        strong_password = "SecurePass123!"
        
        weak_valid, weak_errors = password_manager.validate_password_strength(weak_password)
        strong_valid, strong_errors = password_manager.validate_password_strength(strong_password)
        
        if not weak_valid and strong_valid:
            print("   ✅ Password strength validation working")
            print(f"   📊 Weak password errors: {len(weak_errors)}")
            
            # Test password hashing
            hashed = password_manager.hash_password(strong_password)
            verified = password_manager.verify_password(strong_password, hashed)
            
            if verified:
                print("   ✅ Password hashing and verification working")
                
                # Test password generation
                generated_password = password_manager.generate_secure_password(16)
                gen_valid, gen_errors = password_manager.validate_password_strength(generated_password)
                
                if gen_valid:
                    print("   ✅ Secure password generation working")
                    print(f"   📊 Generated password length: {len(generated_password)}")
                    return True
        
        return False
        
    except Exception as e:
        print(f"   ❌ Password security test failed: {e}")
        return False


async def test_mfa_functionality():
    """Test Multi-Factor Authentication"""
    print("\n📱 Testing Multi-Factor Authentication...")
    
    try:
        auth_manager = AuthenticationManager()
        mfa_manager = auth_manager.mfa_manager
        
        # Test MFA secret generation
        user_id = "mfa_test_user"
        mfa_secret = mfa_manager.generate_mfa_secret(user_id)
        
        if mfa_secret:
            print("   ✅ MFA secret generation successful")
            
            # Test QR code URL generation
            qr_url = mfa_manager.generate_qr_code_url("test@example.com", mfa_secret)
            if qr_url and "otpauth://" in qr_url:
                print("   ✅ QR code URL generation successful")
                
                # Test backup codes generation
                backup_codes = mfa_manager.generate_backup_codes(5)
                if len(backup_codes) == 5:
                    print("   ✅ Backup codes generation successful")
                    print(f"   📊 Sample backup code: {backup_codes[0]}")
                    return True
        
        return False
        
    except Exception as e:
        print(f"   ❌ MFA functionality test failed: {e}")
        return False


async def test_security_performance():
    """Test security performance"""
    print("\n⚡ Testing Security Performance...")
    
    try:
        start_time = datetime.now()
        
        # Test concurrent authentication
        auth_manager = AuthenticationManager()
        tasks = []
        
        for i in range(10):
            credentials = UserCredentials(
                email=f"perf_test_{i}@example.com",
                username=f"perf_user_{i}",
                password="TestPass123!"
            )
            
            task = asyncio.create_task(auth_manager.register_user(credentials))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        successful_registrations = sum(1 for r in results if r.success)
        
        # Test concurrent authorization
        auth_engine = AuthorizationEngine()
        auth_tasks = []
        
        for i in range(20):
            request = AccessRequest(
                user_id=f"perf_user_{i % 10}",
                resource_type=ResourceType.PROJECT,
                action=ActionType.READ,
                context={"hour": 14}
            )
            
            task = asyncio.create_task(auth_engine.authorize(request))
            auth_tasks.append(task)
        
        auth_results = await asyncio.gather(*auth_tasks)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        throughput = (len(tasks) + len(auth_tasks)) / processing_time
        
        print(f"   📊 Successful registrations: {successful_registrations}/10")
        print(f"   📊 Authorization requests: {len(auth_results)}")
        print(f"   📊 Processing time: {processing_time:.3f}s")
        print(f"   📊 Throughput: {throughput:.2f} operations/second")
        
        return throughput > 50  # Good performance threshold
        
    except Exception as e:
        print(f"   ❌ Security performance test failed: {e}")
        return False


if __name__ == "__main__":
    print("🔒 Starting TRM-OS Phase 3 Security Framework Test...")
    
    async def main():
        # Main security framework test
        framework_results = await test_security_framework()
        
        # Additional security tests
        password_result = await test_password_security()
        mfa_result = await test_mfa_functionality()
        performance_result = await test_security_performance()
        
        print(f"\n{'='*80}")
        print("🏁 SECURITY FRAMEWORK TEST COMPLETED")
        print(f"{'='*80}")
        
        # Summary
        total_passed = (
            sum(framework_results.values()) + 
            int(password_result) + 
            int(mfa_result) + 
            int(performance_result)
        )
        total_tests = len(framework_results) + 3
        
        print(f"📊 Total tests passed: {total_passed}/{total_tests}")
        print(f"📊 Success rate: {total_passed/total_tests*100:.1f}%")
        
        if total_passed >= total_tests * 0.9:
            print("🎉 PHASE 3 SECURITY FRAMEWORK: OUTSTANDING!")
            print("🔒 Enterprise-grade security ready for deployment")
        elif total_passed >= total_tests * 0.7:
            print("✅ PHASE 3 SECURITY FRAMEWORK: EXCELLENT!")
            print("🔧 Minor security optimizations recommended")
        else:
            print("⚠️ PHASE 3 SECURITY FRAMEWORK: NEEDS WORK")
            print("🛠️ Security improvements required")
        
        return framework_results
    
    results = asyncio.run(main()) 