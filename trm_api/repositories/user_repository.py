from typing import Optional, List, Tuple
from passlib.context import CryptContext
import math
from trm_api.graph_models.user import User
from trm_api.models.user import UserCreate, UserUpdate # Pydantic model for API data

# Setup password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    """
    Repository for handling all database operations related to Users.
    """

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_user(self, user_data: UserCreate) -> User:
        """
        Creates a new User node in the database with a hashed password.
        """
        try:
            # Create a dictionary from the pydantic model
            user_dict = user_data.model_dump()
            # Hash the password before saving
            user_dict["hashed_password"] = self.get_password_hash(user_dict.pop("password"))
            
            print(f"DEBUG - Tạo User với dữ liệu: {user_dict}")
            
            # Kiểm tra xem Neo4j có kết nối được không
            from neomodel import db
            results, meta = db.cypher_query("MATCH (n) RETURN COUNT(n) LIMIT 1")
            print(f"DEBUG - Kết nối Neo4j OK, số node hiện tại: {results[0][0]}")
            
            graph_user = User(**user_dict).save()
            print(f"DEBUG - Đã tạo User thành công: {graph_user.username}")
            return graph_user
        except Exception as e:
            import traceback
            print(f"ERROR - Lỗi khi tạo User: {str(e)}")
            print(traceback.format_exc())
            raise

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieves a User node by their username.
        """
        try:
            return User.nodes.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.
        """
        try:
            return User.nodes.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user_by_uid(self, uid: str) -> Optional[User]:
        """
        Retrieves a User node by its unique ID.
        """
        try:
            return User.nodes.get(uid=uid)
        except User.DoesNotExist:
            return None

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieves a list of all users with pagination.
        """
        print(f"DEBUG - UserRepository.list_users: Bắt đầu lấy danh sách người dùng. Skip: {skip}, Limit: {limit}")
        try:
            from neomodel import db
            # Kiểm tra kết nối nhanh
            db.cypher_query("MATCH (n:User) RETURN count(n) AS user_count")
            print(f"DEBUG - UserRepository.list_users: Kết nối Neo4j và truy vấn kiểm tra thành công.")
            
            all_users_node_set = User.nodes.all()
            print(f"DEBUG - UserRepository.list_users: Đã gọi User.nodes.all(). Số lượng (ước tính): {len(all_users_node_set)}")
            
            users = all_users_node_set[skip:skip + limit]
            print(f"DEBUG - UserRepository.list_users: Đã cắt danh sách. Số lượng sau khi cắt: {len(users)}")
            
            # Chuyển đổi sang danh sách để đảm bảo không có vấn đề lazy loading
            user_list = list(users)
            print(f"DEBUG - UserRepository.list_users: Hoàn thành, trả về {len(user_list)} người dùng.")
            return user_list
        except Exception as e:
            import traceback
            print(f"ERROR - UserRepository.list_users: Lỗi khi lấy danh sách người dùng: {str(e)}")
            print(traceback.format_exc())
            # Trả về danh sách rỗng trong trường hợp lỗi để tránh treo API
            return []
            
    def get_paginated_users(self, page: int = 1, page_size: int = 10) -> Tuple[List[User], int, int]:
        """
        Retrieves a paginated list of all users with total count and page count.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            Tuple of (users, total_count, page_count)
        """
        print(f"DEBUG - UserRepository.get_paginated_users: Bắt đầu lấy danh sách người dùng phân trang. Page: {page}, Page Size: {page_size}")
        try:
            from neomodel import db
            # Kiểm tra kết nối nhanh
            results, meta = db.cypher_query("MATCH (n:User) RETURN count(n) AS user_count")
            total_count = results[0][0]
            print(f"DEBUG - UserRepository.get_paginated_users: Kết nối Neo4j thành công. Tổng số người dùng: {total_count}")
            
            # Tính toán số trang
            page_count = math.ceil(total_count / page_size) if total_count > 0 else 1
            
            # Tính toán offset dựa trên page và page_size
            offset = (page - 1) * page_size
            
            # Lấy danh sách người dùng theo phân trang
            all_users = list(User.nodes.all())
            paginated_users = all_users[offset:offset + page_size]
            
            print(f"DEBUG - UserRepository.get_paginated_users: Hoàn thành, trả về {len(paginated_users)} người dùng, trang {page}/{page_count}")
            return paginated_users, total_count, page_count
        except Exception as e:
            import traceback
            print(f"ERROR - UserRepository.get_paginated_users: Lỗi khi lấy danh sách người dùng phân trang: {str(e)}")
            print(traceback.format_exc())
            # Trả về danh sách rỗng trong trường hợp lỗi để tránh treo API
            return [], 0, 0

    def update_user(self, uid: str, user_data: UserUpdate) -> Optional[User]:
        """
        Updates an existing user.
        Note: Does not support password changes through this method for security.
        """
        user = self.get_user_by_uid(uid)
        if not user:
            return None

        # Use by_alias=True to ensure the dictionary keys match the GraphModel's property names
        update_data = user_data.model_dump(exclude_unset=True, by_alias=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.save()
        return user

    def delete_user(self, uid: str) -> bool:
        """
        Deletes a user by their unique ID.
        """
        user = self.get_user_by_uid(uid)
        if not user:
            return False
        
        user.delete()
        return True
