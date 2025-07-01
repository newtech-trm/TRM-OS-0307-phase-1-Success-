import sys
import os
import logging
import json
import argparse
import datetime
from typing import Dict, Any, List, Optional
from neo4j import GraphDatabase

# Thêm thư mục gốc của project vào sys.path để có thể import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trm_api.adapters.data_adapters import BaseEntityAdapter
from trm_api.adapters.entity_adapters import (
    WinAdapter, 
    RecognitionAdapter, 
    TaskAdapter, 
    EventAdapter,
    KnowledgeSnippetAdapter
)
from trm_api.models.enums import EntityType
from trm_api.core.config import settings

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ontology_migration.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ontology_migration")

class OntologyMigrationTool:
    """Công cụ migration dữ liệu legacy trong Neo4j để đồng bộ với chuẩn ontology V3.2."""
    
    def __init__(self, uri, username, password, database="neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
        self.adapters = {
            EntityType.WIN: WinAdapter(),
            EntityType.RECOGNITION: RecognitionAdapter(),
            EntityType.TASK: TaskAdapter(),
            EntityType.EVENT: EventAdapter(),
            EntityType.KNOWLEDGE_SNIPPET: KnowledgeSnippetAdapter()
        }
        
        self.migration_stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "entity_stats": {}
        }
        
        for entity_type in EntityType:
            self.migration_stats["entity_stats"][entity_type.value] = {
                "total": 0,
                "success": 0,
                "failed": 0,
                "skipped": 0
            }
    
    def close(self):
        self.driver.close()
    
    def run_query(self, query, parameters=None):
        with self.driver.session(database=self.database) as session:
            return session.run(query, parameters or {}).data()
    
    def update_node(self, node_id, properties):
        query = """
        MATCH (n) WHERE id(n) = $node_id
        SET n += $properties
        RETURN n
        """
        return self.run_query(query, {"node_id": node_id, "properties": properties})
    
    def get_all_entities(self, entity_type: EntityType, limit: Optional[int] = None, skip: Optional[int] = 0):
        """Lấy tất cả các entity theo loại từ Neo4j."""
        label = entity_type.value.capitalize()
        
        limit_clause = f"LIMIT {limit}" if limit is not None else ""
        skip_clause = f"SKIP {skip}" if skip > 0 else ""
        
        query = f"""
        MATCH (n:{label})
        RETURN n, id(n) as node_id
        {skip_clause}
        {limit_clause}
        """
        
        return self.run_query(query)
    
    def migrate_entity(self, entity_data: Dict[str, Any], entity_type: EntityType) -> Dict[str, Any]:
        """Áp dụng adapter để chuẩn hóa dữ liệu entity theo ontology."""
        adapter = self.adapters.get(entity_type)
        if not adapter:
            logger.warning(f"Không tìm thấy adapter cho entity type {entity_type}")
            return entity_data
        
        try:
            # Áp dụng adapter để chuẩn hóa dữ liệu
            normalized_data = adapter.apply_to_entity(entity_data)
            return normalized_data
        except Exception as e:
            logger.error(f"Lỗi khi chuẩn hóa {entity_type} với uid={entity_data.get('uid')}: {str(e)}")
            return entity_data
    
    def process_entity_batch(self, entity_type: EntityType, dry_run: bool = True, batch_size: int = 100):
        """Xử lý migration cho một loại entity theo batch."""
        count = 0
        skip = 0
        
        while True:
            entities = self.get_all_entities(entity_type, limit=batch_size, skip=skip)
            if not entities:
                break
                
            logger.info(f"Xử lý batch {skip//batch_size + 1} với {len(entities)} {entity_type.value}")
            
            for entity_record in entities:
                count += 1
                self.migration_stats["total"] += 1
                self.migration_stats["entity_stats"][entity_type.value]["total"] += 1
                
                node = entity_record["n"]
                node_id = entity_record["node_id"]
                
                entity_data = dict(node.items())
                
                try:
                    # Chuẩn hóa dữ liệu theo ontology
                    normalized_data = self.migrate_entity(entity_data, entity_type)
                    
                    # Kiểm tra xem data có thay đổi không
                    changes = {}
                    for key, value in normalized_data.items():
                        if key in entity_data and entity_data[key] != value:
                            changes[key] = value
                    
                    if changes:
                        logger.info(f"Các thay đổi cho {entity_type.value} (uid={entity_data.get('uid')}): {json.dumps(changes)}")
                        
                        if not dry_run:
                            # Cập nhật vào Neo4j
                            self.update_node(node_id, changes)
                            logger.info(f"Đã cập nhật {entity_type.value} với uid={entity_data.get('uid')}")
                            self.migration_stats["success"] += 1
                            self.migration_stats["entity_stats"][entity_type.value]["success"] += 1
                        else:
                            logger.info(f"[DRY RUN] Sẽ cập nhật {entity_type.value} với uid={entity_data.get('uid')}")
                            self.migration_stats["skipped"] += 1
                            self.migration_stats["entity_stats"][entity_type.value]["skipped"] += 1
                    else:
                        logger.debug(f"Không có thay đổi cho {entity_type.value} với uid={entity_data.get('uid')}")
                        self.migration_stats["skipped"] += 1
                        self.migration_stats["entity_stats"][entity_type.value]["skipped"] += 1
                
                except Exception as e:
                    logger.error(f"Lỗi khi xử lý {entity_type.value} với uid={entity_data.get('uid')}: {str(e)}")
                    self.migration_stats["failed"] += 1
                    self.migration_stats["entity_stats"][entity_type.value]["failed"] += 1
            
            skip += batch_size
            
            if len(entities) < batch_size:
                break
        
        logger.info(f"Đã xử lý tổng cộng {count} {entity_type.value}")
        return count
    
    def run_migration(self, entity_types=None, dry_run=True, batch_size=100):
        """Chạy migration cho các entity types được chỉ định."""
        start_time = datetime.datetime.now()
        logger.info(f"Bắt đầu migration ontology vào {start_time}")
        logger.info(f"Chế độ DRY RUN: {dry_run}")
        
        if not entity_types:
            entity_types = list(EntityType)
        
        total_count = 0
        for entity_type in entity_types:
            logger.info(f"Bắt đầu migration cho {entity_type.value}")
            count = self.process_entity_batch(entity_type, dry_run, batch_size)
            total_count += count
            logger.info(f"Hoàn thành migration cho {entity_type.value}. Đã xử lý {count} records.")
        
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        logger.info(f"Migration hoàn tất. Tổng thời gian: {duration}")
        logger.info(f"Tổng số records đã xử lý: {total_count}")
        logger.info(f"Thống kê: {json.dumps(self.migration_stats, indent=2)}")


def parse_args():
    parser = argparse.ArgumentParser(description='Công cụ migration dữ liệu legacy trong Neo4j theo chuẩn Ontology V3.2')
    parser.add_argument('--uri', default=settings.NEO4J_URI, help='Neo4j URI')
    parser.add_argument('--user', default=settings.NEO4J_USER, help='Neo4j username')
    parser.add_argument('--password', default=settings.NEO4J_PASSWORD, help='Neo4j password')
    parser.add_argument('--database', default=settings.NEO4J_DATABASE, help='Neo4j database name')
    parser.add_argument('--entity-types', nargs='+', choices=[e.value for e in EntityType], 
                      help='Specific entity types to migrate')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size for processing')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode without making changes')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    # Chuyển đổi tên entity types thành enum
    entity_types = None
    if args.entity_types:
        entity_types = []
        for entity_name in args.entity_types:
            for entity_type in EntityType:
                if entity_type.value == entity_name:
                    entity_types.append(entity_type)
    
    migration_tool = OntologyMigrationTool(
        uri=args.uri,
        username=args.user,
        password=args.password,
        database=args.database
    )
    
    try:
        migration_tool.run_migration(
            entity_types=entity_types,
            dry_run=args.dry_run,
            batch_size=args.batch_size
        )
    except Exception as e:
        logger.error(f"Lỗi không xử lý được trong quá trình migration: {str(e)}")
        sys.exit(1)
    finally:
        migration_tool.close()
