#!/usr/bin/env python3
"""
Script kiểm tra trực tiếp cấu trúc Neo4j để xác minh triển khai ontology-first
"""
import sys
sys.path.append('.')

# Import chỉ các module cần thiết để tránh lỗi
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load các biến môi trường
load_dotenv()

# Lấy thông tin kết nối từ biến môi trường
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

print(f"Kết nối tới Neo4j URI: {neo4j_uri}")

# Tạo driver kết nối trực tiếp thay vì qua neomodel
driver = GraphDatabase.driver(
    neo4j_uri,
    auth=(neo4j_user, neo4j_password)
)

def check_ontology_structure():
    """Kiểm tra cấu trúc ontology trong Neo4j"""
    print("\n=== KIỂM TRA CẤU TRÚC ONTOLOGY TRONG NEO4J ===")
    
    with driver.session() as session:
        # 1. Kiểm tra các Node Label
        print("\n1. Node Labels trong database:")
        result = session.run('CALL db.labels()')
        labels = [record["label"] for record in result]
        print(labels)
        
        # Kiểm tra các entities chính trong ontology
        expected_entities = ["Win", "Recognition", "Event", "KnowledgeSnippet", "Agent", "Task", "Project"]
        missing_entities = [entity for entity in expected_entities if entity not in labels]
        if missing_entities:
            print(f"❌ Thiếu các entity trong database: {missing_entities}")
        else:
            print("✅ Tất cả các entity chính đều tồn tại trong database")
        
        # 2. Kiểm tra các Relationship Type
        print("\n2. Relationship Types trong database:")
        result = session.run('CALL db.relationshipTypes()')
        rel_types = [record["relationshipType"] for record in result]
        print(rel_types)
        
        # Kiểm tra các relationships chính trong ontology
        expected_relationships = ["LEADS_TO_WIN", "RECOGNIZES_WIN", "GENERATES_KNOWLEDGE", "GENERATES_EVENT", "GIVEN_BY", "RECEIVED_BY"]
        missing_relationships = [rel for rel in expected_relationships if rel not in rel_types]
        if missing_relationships:
            print(f"❌ Thiếu các relationship trong database: {missing_relationships}")
        else:
            print("✅ Tất cả các relationship chính đều tồn tại trong database")
        
        # 3. Kiểm tra thuộc tính của entity Win
        print("\n3. Thuộc tính của entity Win:")
        result = session.run("""
        MATCH (w:Win) WHERE w.uuid IS NOT NULL
        RETURN w LIMIT 1
        """)
        win = result.single()
        if win:
            win_properties = list(win[0].keys())
            print(f"Win properties: {win_properties}")
            
            # Kiểm tra các thuộc tính bắt buộc của Win theo ontology
            required_win_props = ["uuid", "name", "narrative", "status", "winType", "created_at"]
            missing_props = [prop for prop in required_win_props if prop not in win_properties]
            if missing_props:
                print(f"❌ Thiếu các thuộc tính của Win: {missing_props}")
            else:
                print("✅ Win có đầy đủ các thuộc tính bắt buộc")
        else:
            print("❌ Không tìm thấy Win nào trong database")
        
        # 4. Kiểm tra relationship LEADS_TO_WIN
        print("\n4. Kiểm tra relationship LEADS_TO_WIN:")
        result = session.run("""
        MATCH (src)-[r:LEADS_TO_WIN]->(w:Win)
        RETURN type(src) as sourceType, src.name as sourceName, w.name as winName
        LIMIT 5
        """)
        leads_to_win = [dict(record) for record in result]
        
        if leads_to_win:
            print(f"LEADS_TO_WIN relationships (tối đa 5):")
            for rel in leads_to_win:
                print(f"  - {rel.get('sourceType', 'Unknown')}({rel.get('sourceName', 'Unnamed')}) --[LEADS_TO_WIN]--> Win({rel.get('winName', 'Unnamed')})")
            print("✅ Relationship LEADS_TO_WIN tồn tại và được sử dụng")
        else:
            print("❌ Không tìm thấy relationship LEADS_TO_WIN nào trong database")

        # 5. Kiểm tra triển khai enum
        print("\n5. Kiểm tra triển khai enum cho Win Status:")
        result = session.run("""
        MATCH (w:Win)
        RETURN DISTINCT w.status as status
        """)
        status_values = [record["status"] for record in result if record["status"] is not None]
        print(f"Win status values: {status_values}")
        
        # 6. Kiểm tra số lượng node cho mỗi entity
        print("\n6. Thống kê số lượng node cho mỗi entity:")
        for entity in expected_entities:
            result = session.run(f"MATCH (n:{entity}) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"  - {entity}: {count} nodes")

def main():
    print("KIỂM TRA TRỰC TIẾP CẤU TRÚC NEO4J THEO ONTOLOGY-FIRST")
    print("=====================================================")
    
    try:
        check_ontology_structure()
        
        print("\n=== KẾT LUẬN ===")
        print("Kiểm tra hoàn tất! Xem các dấu ✅ và ❌ ở trên để biết chi tiết kết quả.")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình kiểm tra: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Đóng kết nối Neo4j
        driver.close()

if __name__ == "__main__":
    main()
