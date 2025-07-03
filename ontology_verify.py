#!/usr/bin/env python3
"""
Script kiểm tra thực tế tính hoạt động của hệ thống theo ontology-first

Script này sẽ:
1. Kết nối trực tiếp tới Neo4j
2. Thực hiện các truy vấn Cypher để kiểm tra cấu trúc ontology
3. Kiểm tra các relationship quan trọng như LEADS_TO_WIN
4. Kiểm tra API thông qua kết nối trực tiếp tới FastAPI app
"""

import sys
import asyncio
sys.path.append('.')

from trm_api.db.session import connect_to_db, get_driver
from trm_api.main import app
from httpx import AsyncClient, ASGITransport

# Kết nối Neo4j
connect_to_db()
driver = get_driver()

async def test_ontology_structure():
    """Kiểm tra cấu trúc ontology trong Neo4j"""
    print("\n=== KIỂM TRA CẤU TRÚC ONTOLOGY TRONG NEO4J ===")
    # Kiểm tra các Node Label
    with driver.session() as session:
        result = session.run('CALL db.labels()')
        labels = [record["label"] for record in result]
        print(f"\nCác Node Labels trong Neo4j: {labels}")
        
        # Kiểm tra các Relationship Type
        result = session.run('CALL db.relationshipTypes()')
        rel_types = [record["relationshipType"] for record in result]
        print(f"\nCác Relationship Types trong Neo4j: {rel_types}")
        
        # Kiểm tra các node Win
        print("\n--- KIỂM TRA WIN ---")
        result = session.run('MATCH (w:Win) RETURN w.uuid as uuid, w.name as name, w.status as status, w.winType as type LIMIT 5')
        wins = [dict(record) for record in result]
        print(f"Các Win trong hệ thống:")
        for win in wins:
            print(f"  - {win}")
        
        # Kiểm tra relationship LEADS_TO_WIN
        print("\n--- KIỂM TRA RELATIONSHIP LEADS_TO_WIN ---")
        result = session.run('MATCH (e)-[r:LEADS_TO_WIN]->(w:Win) RETURN type(e) as sourceType, e.name as sourceName, w.name as winName LIMIT 5')
        leads_to_win = [dict(record) for record in result]
        print(f"Các relationship LEADS_TO_WIN trong hệ thống:")
        for rel in leads_to_win:
            print(f"  - {rel['sourceType']}({rel['sourceName']}) --[LEADS_TO_WIN]--> Win({rel['winName']})")

async def test_api_integration():
    """Kiểm tra API endpoints dựa trên ontology"""
    print("\n=== KIỂM TRA API INTEGRATION ===")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Lấy danh sách Win
        print("\n--- GET /api/v1/wins ---")
        response = await client.get("/api/v1/wins")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Số lượng Win: {len(data)}")
            if data:
                print(f"Win đầu tiên: {data[0]}")
        
        # Lấy danh sách LEADS_TO_WIN relationships
        print("\n--- GET /api/v1/events/relationships/leads_to_win ---")
        response = await client.get("/api/v1/events/relationships/leads_to_win")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Số lượng relationship: {len(data)}")
            if data:
                print(f"Relationship đầu tiên: {data[0]}")

async def main():
    print("KIỂM TRA TOÀN DIỆN ONTOLOGY-FIRST")
    print("=================================")
    
    try:
        # Kiểm tra cấu trúc ontology trong Neo4j
        await test_ontology_structure()
        
        # Kiểm tra API integration
        await test_api_integration()
        
        print("\n=== KẾT QUẢ CHUNG ===")
        print("✅ Kiểm tra hoàn tất!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
