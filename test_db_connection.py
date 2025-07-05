#!/usr/bin/env python3
"""
Script test database connection và agent repository
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_db_connection():
    """Test database connection và agent operations"""
    try:
        print("🔍 Testing Database Connection...")
        
        # Test import
        from trm_api.graph_models.agent import Agent as GraphAgent
        from trm_api.repositories.agent_repository import AgentRepository
        print("✅ Imports successful")
        
        # Test database connection
        try:
            from neomodel import db
            results, meta = db.cypher_query("RETURN 1 as test")
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        
        # Test agent repository
        repo = AgentRepository()
        print("✅ Agent repository created")
        
        # Test list agents
        try:
            agents = await repo.list_agents(skip=0, limit=5)
            print(f"✅ List agents successful: {len(agents)} agents found")
            
            for i, agent in enumerate(agents[:3]):  # Show first 3
                print(f"  {i+1}. {agent.name} ({agent.agent_type})")
                
        except Exception as e:
            print(f"❌ List agents failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 Testing TRM-OS Database Connection")
    print("=" * 50)
    
    success = await test_db_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Database test PASSED!")
        sys.exit(0)
    else:
        print("⚠️  Database test FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 