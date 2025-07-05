#!/usr/bin/env python3
"""
Script kiểm tra environment variables
"""
import os

def check_env():
    """Check environment variables"""
    print("🔍 Checking Environment Variables")
    print("=" * 50)
    
    required_vars = [
        "NEO4J_URI",
        "NEO4J_USER", 
        "NEO4J_PASSWORD",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_KEY",
        "SUPABASE_DB_PASSWORD",
        "RABBITMQ_CLOUD_URL"
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive data
            if any(sensitive in var.lower() for sensitive in ['password', 'key', 'secret']):
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    print("\n" + "=" * 50)
    if missing_vars:
        print(f"⚠️  Missing {len(missing_vars)} environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    else:
        print("🎉 All required environment variables are set!")
        return True

if __name__ == "__main__":
    check_env() 