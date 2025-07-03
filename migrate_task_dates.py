import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Thêm thư mục gốc vào sys.path để import các module khác
sys.path.append('.')

# Load các biến môi trường từ file .env
load_dotenv()

# Lấy thông tin kết nối từ biến môi trường
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

print(f"Connecting to Neo4j URI: {neo4j_uri}")

# Tạo driver kết nối
driver = GraphDatabase.driver(
    neo4j_uri,
    auth=(neo4j_user, neo4j_password)
)

def migrate_task_properties():
    """Di chuyển dữ liệu cho các thuộc tính datetime của Task."""
    print("\n=== BẮT ĐẦU DI CHUYỂN DỮ LIỆU TASK ===")
    
    # Truy vấn Cypher để đổi tên thuộc tính
    # 1. SET: Tạo thuộc tính mới (created_at, updated_at) từ giá trị của thuộc tính cũ.
    # 2. REMOVE: Xóa thuộc tính cũ (creation_date, last_modified_date).
    # 3. WHERE: Chỉ thực hiện trên các node có thuộc tính cũ để tránh lỗi.
    migration_query = """
    MATCH (t:Task)
    WHERE t.creation_date IS NOT NULL OR t.last_modified_date IS NOT NULL
    SET t.created_at = t.creation_date, t.updated_at = t.last_modified_date
    REMOVE t.creation_date, t.last_modified_date
    RETURN count(t) as updated_count
    """
    
    with driver.session() as session:
        try:
            result = session.run(migration_query)
            summary = result.consume()
            updated_count = summary.counters.nodes_created  # Should be 0, we are updating
            
            # Let's get the returned value correctly
            result = session.run(migration_query) # Rerun to get the value
            record = result.single()
            count = record['updated_count'] if record else 0

            print(f"\n✅ Di chuyển dữ liệu thành công!")
            print(f"   - Số lượng Task đã được cập nhật: {count}")
            
        except Exception as e:
            print(f"\n❌ Lỗi trong quá trình di chuyển dữ liệu: {e}")

def main():
    try:
        migrate_task_properties()
    finally:
        driver.close()
        print("\nConnection to Neo4j closed.")

if __name__ == "__main__":
    main()
