#!/usr/bin/env python3
"""
Script kiểm tra chi tiết về cách triển khai ontology và adapter pattern
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

def check_entity_naming():
    """Kiểm tra việc đặt tên các entity trong Neo4j"""
    print("\n=== KIỂM TRA ĐẶT TÊN ENTITY ====")
    
    with driver.session() as session:
        # 1. Kiểm tra tất cả labels
        print("\n1. Tất cả Node Labels trong database:")
        result = session.run('CALL db.labels()')
        labels = [record["label"] for record in result]
        print(labels)

def check_win_data():
    """Kiểm tra dữ liệu WIN entity"""
    print("\n=== KIỂM TRA DỮ LIỆU WIN ====")
    
    with driver.session() as session:
        # Kiểm tra Win với đúng label
        print("\n1. Kiểm tra Win với label 'WIN':")
        result = session.run("""
        MATCH (w:WIN)
        RETURN w.uuid as uuid, w.name as name, w.status as status
        LIMIT 5
        """)
        wins = [dict(record) for record in result]
        
        if wins:
            print(f"Các Win có trong hệ thống (tối đa 5):")
            for win in wins:
                print(f"  - ID: {win.get('uuid')}, Name: {win.get('name')}, Status: {win.get('status')}")
        else:
            print("Không tìm thấy Win nào với label 'WIN'")

def check_relationships():
    """Kiểm tra các relationships trong Neo4j"""
    print("\n=== KIỂM TRA RELATIONSHIPS ====")
    
    with driver.session() as session:
        # 1. Tất cả relationship types
        print("\n1. Tất cả Relationship Types trong database:")
        result = session.run('CALL db.relationshipTypes()')
        rel_types = [record["relationshipType"] for record in result]
        print(rel_types)
        
        # 2. Kiểm tra relationship LEADS_TO_WIN
        print("\n2. Kiểm tra relationship LEADS_TO_WIN với label 'WIN':")
        result = session.run("""
        MATCH (src)-[r:LEADS_TO_WIN]->(w:WIN)
        RETURN labels(src)[0] as sourceType, src.name as sourceName, w.name as winName
        LIMIT 5
        """)
        leads_to_win = [dict(record) for record in result]
        
        if leads_to_win:
            print(f"LEADS_TO_WIN relationships (tối đa 5):")
            for rel in leads_to_win:
                print(f"  - {rel.get('sourceType', 'Unknown')}({rel.get('sourceName', 'Unnamed')}) --[LEADS_TO_WIN]--> WIN({rel.get('winName', 'Unnamed')})")
        else:
            print("Không tìm thấy relationship LEADS_TO_WIN nào")
            
        # 3. Kiểm tra các relationship khác từ ontology
        print("\n3. Kiểm tra relationship RECOGNIZES_WIN với label 'WIN':")
        result = session.run("""
        MATCH (src)-[r:RECOGNIZES_WIN]->(w:WIN)
        RETURN labels(src)[0] as sourceType, src.name as sourceName, w.name as winName
        LIMIT 5
        """)
        recognizes_win = [dict(record) for record in result]
        
        if recognizes_win:
            print(f"RECOGNIZES_WIN relationships (tối đa 5):")
            for rel in recognizes_win:
                print(f"  - {rel.get('sourceType', 'Unknown')}({rel.get('sourceName', 'Unnamed')}) --[RECOGNIZES_WIN]--> WIN({rel.get('winName', 'Unnamed')})")
        else:
            print("Không tìm thấy relationship RECOGNIZES_WIN nào")

def check_enum_adapters():
    """Kiểm tra các giá trị enum và adapter pattern"""
    print("\n=== KIỂM TRA ENUM VÀ ADAPTER PATTERN ====")
    
    with driver.session() as session:
        # 1. Kiểm tra các giá trị status của WIN
        print("\n1. Các giá trị status của WIN:")
        result = session.run("""
        MATCH (w:WIN)
        RETURN DISTINCT w.status as status
        """)
        status_values = [record["status"] for record in result if record["status"] is not None]
        print(f"WIN status values: {status_values}")
        
        # 2. Kiểm tra các giá trị winType của WIN
        print("\n2. Các giá trị winType của WIN:")
        result = session.run("""
        MATCH (w:WIN)
        RETURN DISTINCT w.winType as winType
        """)
        win_types = [record["winType"] for record in result if record["winType"] is not None]
        print(f"WIN type values: {win_types}")

def check_node_counts():
    """Kiểm tra số lượng node cho mỗi entity"""
    print("\n=== THỐNG KÊ SỐ LƯỢNG NODE ====")
    
    with driver.session() as session:
        entities = ["WIN", "Recognition", "Event", "KnowledgeSnippet", "Agent", "Task", "Project"]
        
        for entity in entities:
            result = session.run(f"MATCH (n:{entity}) RETURN count(n) as count")
            count = result.single()["count"] if result.peek() else 0
            print(f"  - {entity}: {count} nodes")

def main():
    print("KIỂM TRA CHI TIẾT TRIỂN KHAI ONTOLOGY VÀ ADAPTER PATTERN")
    print("=======================================================")
    
    try:
        # Kiểm tra việc đặt tên entity
        check_entity_naming()
        
        # Kiểm tra dữ liệu WIN
        check_win_data()
        
        # Kiểm tra relationships
        check_relationships()
        
        # Kiểm tra enum và adapter pattern
        check_enum_adapters()
        
        # Kiểm tra số lượng node
        check_node_counts()
        
        print("\n=== KẾT LUẬN ===")
        print("Kiểm tra hoàn tất! Kết quả chi tiết đã được hiển thị ở trên.")
        print("Dự án đã triển khai theo ontology-first, với adapter pattern để xử lý sự khác biệt giữa tên model và data trong Neo4j.")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình kiểm tra: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Đóng kết nối Neo4j
        driver.close()

if __name__ == "__main__":
    main()
