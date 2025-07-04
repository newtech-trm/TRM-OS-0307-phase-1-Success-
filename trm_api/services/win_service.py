from neo4j import Driver
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import traceback
import uuid
import asyncio

from trm_api.db.session import get_driver
from trm_api.models.win import Win, WinCreate, WinUpdate, WinInDB

class WinService:
    """
    Service layer for handling business logic related to WINs.
    """

    async def _get_db(self) -> Driver:
        return get_driver()

    def _convert_neo4j_types(self, data: Any) -> Any:
        """Recursively convert Neo4j types to Python native types"""
        logging.debug(f"Converting Neo4j types: {type(data)} - {data}")
        
        # Handle None
        if data is None:
            return None
            
        # Handle dictionary
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                logging.debug(f"Processing dict key {key}: {type(value)} - {value}")
                result[key] = self._convert_neo4j_types(value)
            return result
            
        # Handle list 
        if isinstance(data, list):
            result = []
            for item in data:
                logging.debug(f"Processing list item: {type(item)} - {item}")
                result.append(self._convert_neo4j_types(item))
            return result
            
        # Handle Neo4j DateTime - most important case
        if hasattr(data, 'to_native'):
            logging.debug(f"Converting Neo4j DateTime: {data} to native")
            return data.to_native()
            
        # No conversion needed
        return data

    async def create_win(self, win_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logging.debug(f"Creating WIN with data: {win_data}")
            
            # Convert Pydantic model to a regular dictionary if needed
            if hasattr(win_data, 'model_dump'):
                win_dict = win_data.model_dump()
                logging.debug(f"WIN dict after conversion: {win_dict}")
            else:
                win_dict = win_data
                
            logging.debug(f"Creating WIN with params: {win_dict}")
            
            db = await self._get_db()
            with db.session() as session:
                try:
                    # Execute the transaction - Neo4j không hỗ trợ async/await trực tiếp
                    raw_result = session.write_transaction(self._create_win_tx, win_dict)
                    logging.debug(f"Raw result from Neo4j: {raw_result}")
                    logging.debug(f"Result types: {[(k, type(v)) for k, v in raw_result.items()]}")
                    
                    if not raw_result:
                        logging.error("No result returned from Neo4j transaction")
                        return None
                    # Convert Neo4j types to Python types (especially DateTime)
                    converted_data = self._convert_neo4j_types(raw_result)
                    logging.debug(f"Converted data from Neo4j: {converted_data}")
                    
                    # Handle timestamps specially for reliability
                    for dt_field in ['created_at', 'updated_at']:
                        if dt_field in converted_data and hasattr(converted_data[dt_field], 'to_native'):
                            converted_data[dt_field] = converted_data[dt_field].to_native()
                            logging.debug(f"Specially handling timestamp {dt_field}: {converted_data[dt_field]}")

                    # Create the Win model for validation and return
                    return Win(**converted_data)
                except Exception as e:
                    logging.error(f"Error creating WIN: {e}")
                    raise
        except Exception as e:
            logging.error(f"Error creating WIN: {e}")
            raise

    @staticmethod
    def _create_win_tx(tx, win_data: dict) -> dict:
        """Create a WIN node transaction."""
        create_query = (
            "CREATE (w:WIN {uid: $uid, summary: $summary, description: $description, win_type: $win_type}) "
            "SET w.created_at = datetime(), w.updated_at = datetime() "
            "RETURN w as win"
        )
        
        logging.debug(f"Executing Neo4j query: {create_query} with params: {win_data}")
        
        result = tx.run(
            create_query,
            uid=win_data.get('uid') or str(uuid.uuid4()),
            summary=win_data.get('summary'),
            description=win_data.get('description', ''),
            win_type=win_data.get('win_type', 'standard'),
        )
        
        record = result.single()
        if not record:
            return {}
            
        win_node = record.get('win')
        # Convert Neo4j node to dictionary
        win_data = dict(win_node.items())
        logging.debug(f"WIN data from Neo4j: {win_data}")
        return win_data

    async def get_win(self, win_id: str) -> Optional[Dict[str, Any]]:
        """Get WIN by ID."""
        try:
            db = await self._get_db()
            with db.session() as session:
                # Execute the query
                raw_result = session.read_transaction(self._get_win_by_uid_tx, win_id)
                if not raw_result:
                    return None
                
                # Convert Neo4j types (especially DateTime)
                processed_result = self._convert_neo4j_types(raw_result)
                logging.debug(f"Processed WIN data: {processed_result}")
                
                # Return as a Win model instance
                return Win(**processed_result)
        except Exception as e:
            logging.error(f"Error getting WIN: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _get_win_by_uid_tx(self, tx, uid: str) -> Optional[dict]:
        query = "MATCH (w:WIN {uid: $uid}) RETURN w"
        result = tx.run(query, uid=uid)
        record = result.single()
        return dict(record['w']) if record and record['w'] else None

    async def list_wins(self, skip: int = 0, limit: int = 25) -> List[Win]:
        """Retrieves a list of WINs with pagination theo Ontology V3.2."""
        logging.debug(f"WinService.list_wins: Bắt đầu lấy danh sách WINs. Skip: {skip}, Limit: {limit}")
        try:
            db = await self._get_db()
            with db.session() as session:
                raw_results = session.read_transaction(self._list_wins_tx, skip, limit)
                logging.debug(f"WinService.list_wins: Đã nhận {len(raw_results)} kết quả thô từ Neo4j.")
                
                processed_wins = []
                for raw_win_data in raw_results:
                    # Chuyển đổi các kiểu dữ liệu Neo4j, đặc biệt là DateTime
                    converted_data = self._convert_neo4j_types(raw_win_data)
                    logging.debug(f"WinService.list_wins: Dữ liệu WIN đã chuyển đổi: {converted_data}")
                    processed_wins.append(Win(**converted_data))
                
                logging.debug(f"WinService.list_wins: Hoàn thành, trả về {len(processed_wins)} WINs.")
                return processed_wins
        except Exception as e:
            logging.error(f"WinService.list_wins: Lỗi khi lấy danh sách WINs: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return [] # Trả về danh sách rỗng trong trường hợp lỗi

    @staticmethod
    def _list_wins_tx(tx, skip: int, limit: int) -> List[dict]:
        logging.debug(f"WinService._list_wins_tx: Thực thi truy vấn lấy WINs. Skip: {skip}, Limit: {limit}")
        query = (
            "MATCH (w:WIN) "
            "RETURN w.uid AS uid, w.summary AS summary, w.description AS description, w.win_type AS win_type, "
            "w.created_at AS created_at, w.updated_at AS updated_at, w.status AS status, w.priority AS priority, "
            "w.start_date AS start_date, w.end_date AS end_date, w.target_date AS target_date, w.progress AS progress, "
            "w.owner_id AS owner_id, w.team_id AS team_id, w.tags AS tags, w.properties AS properties "
            "ORDER BY w.created_at DESC "
            "SKIP $skip LIMIT $limit"
        )
        try:
            result = tx.run(query, skip=skip, limit=limit)
            # Trả về danh sách các dict, mỗi dict là một WIN
            # Đảm bảo tất cả các trường được trả về từ truy vấn Cypher
            # Neo4j driver tự động chuyển đổi các kiểu cơ bản (string, int, float, boolean, list, dict)
            # DateTime cần được xử lý đặc biệt sau khi lấy dữ liệu
            win_list = [record.data() for record in result] # record.data() trả về dict của tất cả các trường
            logging.debug(f"WinService._list_wins_tx: Truy vấn thành công, {len(win_list)} WINs được trả về.")
            return win_list
        except Exception as e:
            logging.error(f"WinService._list_wins_tx: Lỗi trong quá trình thực thi Cypher: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return []

    async def update_win(self, win_id: str, win_update: WinUpdate) -> Optional[Win]:
        """Updates an existing WIN theo Ontology V3.2."""
        logging.debug(f"WinService.update_win: Cập nhật WIN với ID {win_id}")
        
        # Chuyển đổi từ Pydantic model sang dict, chỉ lấy các trường được đặt giá trị
        update_data = win_update.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_win(win_id)

        # Cập nhật thời gian chỉnh sửa
        update_data['updated_at'] = datetime.utcnow()
        
        # Chuẩn hóa các giá trị enum theo Ontology V3.2
        if 'win_type' in update_data:
            update_data['win_type'] = update_data['win_type'].value if hasattr(update_data['win_type'], 'value') else update_data['win_type']
            
        if 'status' in update_data:
            update_data['status'] = update_data['status'].value if hasattr(update_data['status'], 'value') else update_data['status']

        try:
            db = await self._get_db()
            with db.session() as session:
                result = session.write_transaction(self._update_win_tx, win_id, update_data)
                if not result:
                    logging.error(f"WinService.update_win: Không tìm thấy WIN với ID {win_id}")
                    return None
                    
                # Chuyển đổi dữ liệu từ Neo4j sang Python types
                converted_result = self._convert_neo4j_types(result)
                
                return Win(**converted_result)
        except Exception as e:
            logging.error(f"WinService.update_win: Lỗi khi cập nhật WIN {win_id}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return None

    @staticmethod
    def _update_win_tx(tx, win_id: str, update_data: dict) -> Optional[dict]:
        """Transaction để cập nhật WIN theo Ontology V3.2."""
        # Xây dựng các mệnh đề SET để cập nhật các trường
        set_clauses = []
        for key, value in update_data.items():
            # Xử lý đặc biệt cho datetime
            if key in ['updated_at', 'created_at', 'start_date', 'end_date', 'target_date'] and value is not None:
                set_clauses.append(f"w.{key} = datetime($update_data.{key})")
            else:
                set_clauses.append(f"w.{key} = $update_data.{key}")

        query = (
            f"MATCH (w:WIN {{uid: $win_id}}) "
            f"SET {', '.join(set_clauses)} "
            "RETURN w"
        )
        
        logging.debug(f"WinService._update_win_tx: Thực thi truy vấn UPDATE: {query}")
        logging.debug(f"WinService._update_win_tx: Với tham số: win_id={win_id}, update_data={update_data}")
        
        result = tx.run(query, win_id=win_id, update_data=update_data)
        record = result.single()
        
        if not record:
            logging.error(f"WinService._update_win_tx: Không tìm thấy WIN với ID {win_id}")
            return None
            
        # Chuyển đổi node Neo4j thành dictionary
        win_data = dict(record['w'].items())
        logging.debug(f"WinService._update_win_tx: Kết quả cập nhật: {win_data}")
        return win_data

    async def delete_win(self, win_id: str) -> bool:
        """Deletes a WIN by its ID theo Ontology V3.2."""
        logging.debug(f"WinService.delete_win: Xóa WIN với ID {win_id}")
        try:
            db = await self._get_db()
            with db.session() as session:
                # Đầu tiên hãy kiểm tra xem WIN có tồn tại không
                win = session.read_transaction(self._get_win_by_uid_tx, win_id)
                if not win:
                    logging.warning(f"WinService.delete_win: Không tìm thấy WIN với ID {win_id}")
                    return False
                    
                # Xóa WIN và tất cả các mối quan hệ liên quan
                result = session.write_transaction(self._delete_win_tx, win_id)
                return result
        except Exception as e:
            logging.error(f"WinService.delete_win: Lỗi khi xóa WIN {win_id}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return False

    @staticmethod
    def _delete_win_tx(tx, win_id: str) -> bool:
        """Transaction để xóa WIN và các mối quan hệ liên quan theo Ontology V3.2."""
        logging.debug(f"WinService._delete_win_tx: Xóa WIN với ID {win_id} và các mối quan hệ liên quan")
        
        # Trước hết, ngắt kết nối các mối quan hệ quan trọng để giữ tính toàn vẹn dữ liệu
        # DETACH DELETE sẽ xóa tất cả các mối quan hệ, nhưng chúng ta có thể kiểm tra trước
        
        # Xóa WIN và tất cả các mối quan hệ liên quan
        query = "MATCH (w:WIN {uid: $win_id}) DETACH DELETE w"
        result = tx.run(query, win_id=win_id)
        summary = result.consume()
        
        deleted_count = summary.counters.nodes_deleted
        logging.debug(f"WinService._delete_win_tx: Đã xóa {deleted_count} node WIN")
        
        return deleted_count > 0

# Singleton instance of the service
win_service = WinService()
