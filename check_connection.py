#!/usr/bin/env python
"""
Script kiểm tra kết nối đến Neo4j Aura và hiển thị dữ liệu thực tế
"""
import sys
sys.path.append('.')

try:
    from trm_api.db.session import get_driver, connect_to_db
    print("Module session được import thành công")
except ImportError as e:
    print(f"Lỗi import module: {e}")
    sys.exit(1)

try:
    # Kết nối thông qua neomodel
    connect_to_db()
    print("Đã kết nối thông qua neomodel")
    
    # Kết nối đến Neo4j Aura bằng driver trực tiếp
    driver = get_driver()
    print("Kết nối đến Neo4j thành công qua driver")
    
    # Kiểm tra thống kê dữ liệu
    with driver.session() as session:
        # Thống kê loại node
        result = session.run('MATCH (n) RETURN labels(n) as Type, count(n) as Count')
        print("\n== Thống kê dữ liệu Neo4j Aura ==")
        for record in result:
            print(f"{record['Type']}: {record['Count']} nodes")
        
        # Lấy danh sách Project
        print("\n== 5 Project mới nhất ==")
        result = session.run('MATCH (p:Project) RETURN p.name as Name, p.description as Description LIMIT 5')
        project_count = 0
        for record in result:
            project_count += 1
            print(f"Project: {record['Name']} - {record['Description']}")
        
        if project_count == 0:
            print("Không tìm thấy Project nào trong database!")
        
        # Lấy danh sách Task
        print("\n== 5 Task mới nhất ==")
        result = session.run('MATCH (t:Task) RETURN t.name as Name, t.description as Description LIMIT 5')
        task_count = 0
        for record in result:
            task_count += 1
            print(f"Task: {record['Name']} - {record['Description']}")
        
        if task_count == 0:
            print("Không tìm thấy Task nào trong database!")
        
        # Kiểm tra Relationship
        print("\n== 5 Relationship mới nhất ==")
        result = session.run('MATCH (a)-[r]->(b) RETURN type(r) as Type, a.name as From, b.name as To LIMIT 5')
        rel_count = 0
        for record in result:
            rel_count += 1
            print(f"Relationship: {record['From']} -[{record['Type']}]-> {record['To']}")
        
        if rel_count == 0:
            print("Không tìm thấy Relationship nào trong database!")
    
    print("\nKiểm tra kết nối thành công!")
    
except Exception as e:
    print(f"Lỗi khi kết nối đến Neo4j: {e}")
    sys.exit(1)
