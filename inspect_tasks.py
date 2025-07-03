import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Thêm thư mục gốc vào sys.path
sys.path.append('.')

# Load các biến môi trường
load_dotenv()

# Thông tin kết nối
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
project_id_to_check = "39c8b90e5f3d4344bae6d1b5ded584fe"

print(f"Connecting to Neo4j: {neo4j_uri}")
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def inspect_task_nodes():
    """Kiểm tra các thuộc tính của node Task trong một dự án cụ thể."""
    print(f"\n=== KIỂM TRA TASK NODES CHO PROJECT_ID: {project_id_to_check} ===")
    
    # Truy vấn Cypher để lấy tất cả thuộc tính của các node Task
    query = """
    MATCH (p:Project {uid: $project_id})-[r:HAS_TASK]->(t:Task)
    RETURN t
    LIMIT 5
    """
    
    with driver.session() as session:
        try:
            result = session.run(query, project_id=project_id_to_check)
            tasks = [record['t'] for record in result]
            
            if not tasks:
                print("\nKhông tìm thấy Task nào cho dự án này.")
                return

            print(f"\nTìm thấy {len(tasks)} task(s). Chi tiết thuộc tính:")
            for i, task in enumerate(tasks):
                print(f"\n--- Task {i+1} (UID: {task.get('uid')}) ---")
                for key, value in task.items():
                    print(f"  - {key}: {value} (type: {type(value).__name__})")
            
        except Exception as e:
            print(f"\n❌ Lỗi trong quá trình kiểm tra: {e}")

def main():
    try:
        inspect_task_nodes()
    finally:
        driver.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    main()
