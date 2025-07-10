#!/usr/bin/env python3
"""
Debug script để test Resource.create_single() method
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_api.graph_models.resource import Resource as GraphResource

def test_resource_creation():
    print("=== Testing Resource.create_single() ===")
    
    # Test create_single method
    print("Calling GraphResource.create_single()...")
    try:
        result = GraphResource.create_single(
            name="Test Resource",
            description="Test description", 
            resourceType="Human"
        )
        
        print(f"Type of result: {type(result)}")
        print(f"Result: {result}")
        
        if isinstance(result, list):
            print(f"Result is a list with {len(result)} items")
            if result:
                print(f"First item type: {type(result[0])}")
                print(f"First item: {result[0]}")
                print(f"First item has assigned_to_projects: {hasattr(result[0], 'assigned_to_projects')}")
        else:
            print(f"Result is not a list")
            print(f"Has assigned_to_projects: {hasattr(result, 'assigned_to_projects')}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== Testing regular GraphResource() ===")
    try:
        resource = GraphResource(
            name="Regular Resource",
            description="Regular description",
            resourceType="Tool"
        ).save()
        
        print(f"Type of resource: {type(resource)}")
        print(f"Resource: {resource}")
        print(f"Has assigned_to_projects: {hasattr(resource, 'assigned_to_projects')}")
        
        # Cleanup
        resource.delete()
        
    except Exception as e:
        print(f"Error in regular creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_resource_creation() 