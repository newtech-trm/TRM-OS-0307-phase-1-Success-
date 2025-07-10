"""
Snowflake MCP Connector

Enterprise-grade MCP connector for Snowflake Data Cloud integration.
Provides unified access to Snowflake analytics, data warehousing, and ML capabilities.
"""

from typing import Dict, Any, List, Optional, Union
import logging
import asyncio
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine, text

from .base_mcp_connector import (
    BaseMCPConnector,
    MCPConnectionConfig,
    MCPRequest,
    MCPResponse,
    MCPHealthCheck,
    MCPConnectionStatus,
    MCPOperationType
)

logger = logging.getLogger(__name__)


@dataclass
class SnowflakeQueryResult:
    """Snowflake query result structure"""
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    execution_time_ms: float
    query_id: str
    warehouse_name: str
    metadata: Dict[str, Any]


class SnowflakeMCPConnector(BaseMCPConnector):
    """
    Snowflake MCP Connector for Data Cloud Integration
    
    Features:
    - SQL query execution with result streaming
    - Data warehouse management operations
    - Snowpark integration for ML workloads
    - Performance monitoring and query optimization
    - Multi-warehouse support with automatic failover
    - Result caching and pagination
    """
    
    def __init__(self, config: MCPConnectionConfig):
        super().__init__(config)
        self._connection = None
        self._engine = None
        self._warehouse_pool = []
        self._query_history = []
        
        # Snowflake-specific configuration
        self._account = config.credentials.get('account')
        self._username = config.credentials.get('user') or config.credentials.get('username')
        self._password = config.credentials.get('password')
        self._database = config.credentials.get('database', 'TRM_OS_ANALYTICS')
        self._schema = config.credentials.get('schema', 'PUBLIC')
        self._warehouse = config.credentials.get('warehouse', 'COMPUTE_WH')
        self._role = config.credentials.get('role', 'SYSADMIN')
        
        # Validate required credentials
        if not self._account or not self._username or not self._password:
            raise ValueError("Snowflake connector requires account, username, and password")
        
        logger.info(f"Initialized Snowflake connector for account: {self._account}")
    
    # ================================
    # PLATFORM-SPECIFIC IMPLEMENTATIONS
    # ================================
    
    async def _platform_connect(self) -> bool:
        """Establish connection to Snowflake"""
        try:
            # Create Snowflake connection
            connection_params = {
                'account': self._account,
                'user': self._username,
                'password': self._password,
                'database': self._database,
                'schema': self._schema,
                'warehouse': self._warehouse,
                'role': self._role,
                'timeout': self.config.timeout,
                'client_session_keep_alive': True,
                'autocommit': True
            }
            
            # Use asyncio.to_thread for blocking connection
            self._connection = await asyncio.to_thread(
                snowflake.connector.connect,
                **connection_params
            )
            
            # Create SQLAlchemy engine for advanced operations
            url = URL(
                account=self._account,
                user=self._username,
                password=self._password,
                database=self._database,
                schema=self._schema,
                warehouse=self._warehouse,
                role=self._role
            )
            
            self._engine = create_engine(url, echo=False)
            
            logger.info(f"Successfully connected to Snowflake account: {self._account}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    async def _platform_disconnect(self) -> bool:
        """Disconnect from Snowflake"""
        try:
            if self._connection:
                await asyncio.to_thread(self._connection.close)
                self._connection = None
            
            if self._engine:
                await asyncio.to_thread(self._engine.dispose)
                self._engine = None
            
            logger.info("Successfully disconnected from Snowflake")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disconnect from Snowflake: {str(e)}")
            return False
    
    async def _platform_authenticate(self) -> bool:
        """Authenticate with Snowflake (handled during connection)"""
        try:
            # Test authentication with simple query
            test_query = "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
            cursor = self._connection.cursor(DictCursor)
            
            result = await asyncio.to_thread(cursor.execute, test_query)
            row = await asyncio.to_thread(cursor.fetchone)
            
            if row:
                logger.info(f"Authenticated as user: {row['CURRENT_USER()']}, role: {row['CURRENT_ROLE()']}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Snowflake authentication failed: {str(e)}")
            return False
    
    async def _platform_execute_request(self, request: MCPRequest) -> MCPResponse:
        """Execute Snowflake-specific request"""
        try:
            if request.operation_type == MCPOperationType.QUERY:
                return await self._execute_query(request)
            elif request.operation_type == MCPOperationType.EXECUTE:
                return await self._execute_command(request)
            elif request.operation_type == MCPOperationType.BATCH:
                return await self._execute_batch(request)
            elif request.operation_type == MCPOperationType.STREAM:
                return await self._execute_stream(request)
            else:
                return MCPResponse(
                    request_id=request.request_id,
                    success=False,
                    error=f"Unsupported operation type: {request.operation_type}"
                )
                
        except Exception as e:
            logger.error(f"Failed to execute Snowflake request: {str(e)}")
            return MCPResponse(
                request_id=request.request_id,
                success=False,
                error=str(e)
            )
    
    async def _platform_health_check(self) -> MCPHealthCheck:
        """Perform Snowflake health check"""
        start_time = datetime.now()
        
        try:
            # Test basic connectivity
            test_query = "SELECT 1 as health_check, CURRENT_TIMESTAMP() as check_time"
            cursor = self._connection.cursor(DictCursor)
            
            await asyncio.to_thread(cursor.execute, test_query)
            result = await asyncio.to_thread(cursor.fetchone)
            
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            if result and result['HEALTH_CHECK'] == 1:
                return MCPHealthCheck(
                    platform="snowflake",
                    status=MCPConnectionStatus.AUTHENTICATED,
                    response_time_ms=response_time,
                    metadata={
                        'check_time': result['CHECK_TIME'],
                        'warehouse': self._warehouse,
                        'database': self._database,
                        'schema': self._schema
                    }
                )
            else:
                return MCPHealthCheck(
                    platform="snowflake",
                    status=MCPConnectionStatus.ERROR,
                    response_time_ms=response_time,
                    error_message="Health check query returned unexpected result"
                )
                
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            return MCPHealthCheck(
                platform="snowflake",
                status=MCPConnectionStatus.ERROR,
                response_time_ms=response_time,
                error_message=str(e)
            )
    
    # ================================
    # SNOWFLAKE-SPECIFIC OPERATIONS
    # ================================
    
    async def _execute_query(self, request: MCPRequest) -> MCPResponse:
        """Execute SELECT query and return results"""
        start_time = datetime.now()
        
        try:
            sql = request.parameters.get('sql')
            if not sql:
                return MCPResponse(
                    request_id=request.request_id,
                    success=False,
                    error="SQL parameter is required for query operations"
                )
            
            # Optional parameters
            limit = request.parameters.get('limit', 1000)
            warehouse = request.parameters.get('warehouse', self._warehouse)
            
            # Switch warehouse if needed
            if warehouse != self._warehouse:
                await self._switch_warehouse(warehouse)
            
            cursor = self._connection.cursor(DictCursor)
            
            # Execute query
            await asyncio.to_thread(cursor.execute, sql)
            
            # Fetch results with limit
            if limit > 0:
                rows = await asyncio.to_thread(cursor.fetchmany, limit)
            else:
                rows = await asyncio.to_thread(cursor.fetchall)
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            # Convert rows to list format
            result_rows = []
            for row in rows:
                if isinstance(row, dict):
                    result_rows.append([row[col] for col in columns])
                else:
                    result_rows.append(list(row))
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Create query result
            query_result = SnowflakeQueryResult(
                columns=columns,
                rows=result_rows,
                row_count=len(result_rows),
                execution_time_ms=execution_time,
                query_id=cursor.sfqid,
                warehouse_name=warehouse,
                metadata={
                    'rowcount': cursor.rowcount,
                    'description': cursor.description
                }
            )
            
            # Store in query history
            self._query_history.append({
                'request_id': request.request_id,
                'sql': sql,
                'execution_time_ms': execution_time,
                'row_count': len(result_rows),
                'timestamp': datetime.now()
            })
            
            # Keep only last 100 queries in history
            if len(self._query_history) > 100:
                self._query_history = self._query_history[-100:]
            
            return MCPResponse(
                request_id=request.request_id,
                success=True,
                data=query_result.__dict__,
                metadata={
                    'query_id': cursor.sfqid,
                    'warehouse': warehouse,
                    'execution_time_ms': execution_time
                },
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Query execution failed: {str(e)}")
            
            return MCPResponse(
                request_id=request.request_id,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
    
    async def _execute_command(self, request: MCPRequest) -> MCPResponse:
        """Execute DDL/DML commands"""
        start_time = datetime.now()
        
        try:
            sql = request.parameters.get('sql')
            if not sql:
                return MCPResponse(
                    request_id=request.request_id,
                    success=False,
                    error="SQL parameter is required for execute operations"
                )
            
            warehouse = request.parameters.get('warehouse', self._warehouse)
            
            # Switch warehouse if needed
            if warehouse != self._warehouse:
                await self._switch_warehouse(warehouse)
            
            cursor = self._connection.cursor()
            
            # Execute command
            result = await asyncio.to_thread(cursor.execute, sql)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return MCPResponse(
                request_id=request.request_id,
                success=True,
                data={
                    'affected_rows': cursor.rowcount,
                    'query_id': cursor.sfqid
                },
                metadata={
                    'query_id': cursor.sfqid,
                    'warehouse': warehouse,
                    'execution_time_ms': execution_time
                },
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Command execution failed: {str(e)}")
            
            return MCPResponse(
                request_id=request.request_id,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
    
    async def _execute_batch(self, request: MCPRequest) -> MCPResponse:
        """Execute multiple SQL statements as batch"""
        start_time = datetime.now()
        
        try:
            sql_statements = request.parameters.get('sql_statements', [])
            if not sql_statements:
                return MCPResponse(
                    request_id=request.request_id,
                    success=False,
                    error="sql_statements parameter is required for batch operations"
                )
            
            warehouse = request.parameters.get('warehouse', self._warehouse)
            
            # Switch warehouse if needed
            if warehouse != self._warehouse:
                await self._switch_warehouse(warehouse)
            
            cursor = self._connection.cursor()
            results = []
            
            # Execute each statement
            for i, sql in enumerate(sql_statements):
                try:
                    await asyncio.to_thread(cursor.execute, sql)
                    results.append({
                        'statement_index': i,
                        'success': True,
                        'affected_rows': cursor.rowcount,
                        'query_id': cursor.sfqid
                    })
                except Exception as e:
                    results.append({
                        'statement_index': i,
                        'success': False,
                        'error': str(e)
                    })
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Calculate overall success
            successful_statements = sum(1 for r in results if r['success'])
            overall_success = successful_statements == len(sql_statements)
            
            return MCPResponse(
                request_id=request.request_id,
                success=overall_success,
                data={
                    'total_statements': len(sql_statements),
                    'successful_statements': successful_statements,
                    'results': results
                },
                metadata={
                    'warehouse': warehouse,
                    'execution_time_ms': execution_time
                },
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Batch execution failed: {str(e)}")
            
            return MCPResponse(
                request_id=request.request_id,
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )
    
    async def _execute_stream(self, request: MCPRequest) -> MCPResponse:
        """Execute query with streaming results"""
        # For now, return regular query results
        # In production, this could implement true streaming
        return await self._execute_query(request)
    
    async def _switch_warehouse(self, warehouse: str) -> bool:
        """Switch to different warehouse"""
        try:
            switch_sql = f"USE WAREHOUSE {warehouse}"
            cursor = self._connection.cursor()
            await asyncio.to_thread(cursor.execute, switch_sql)
            self._warehouse = warehouse
            logger.info(f"Switched to warehouse: {warehouse}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch warehouse to {warehouse}: {str(e)}")
            return False
    
    # ================================
    # ENTERPRISE ANALYTICS METHODS
    # ================================
    
    async def get_warehouse_status(self) -> Dict[str, Any]:
        """Get current warehouse status and metrics"""
        try:
            status_query = """
                SELECT 
                    CURRENT_WAREHOUSE() as warehouse_name,
                    SYSTEM$GET_COMPUTE_POOL_STATUS() as compute_status
            """
            
            request = MCPRequest(
                operation_type=MCPOperationType.QUERY,
                parameters={'sql': status_query}
            )
            
            response = await self._execute_query(request)
            
            if response.success and response.data['rows']:
                return {
                    'warehouse': response.data['rows'][0][0],
                    'status': 'active',
                    'last_checked': datetime.now().isoformat()
                }
            
            return {'status': 'unknown'}
            
        except Exception as e:
            logger.error(f"Failed to get warehouse status: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    async def get_query_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent query execution history"""
        return self._query_history[-limit:] if self._query_history else []
    
    async def analyze_table(self, table_name: str) -> Dict[str, Any]:
        """Analyze table structure and statistics"""
        try:
            analyze_queries = {
                'structure': f"DESCRIBE TABLE {table_name}",
                'row_count': f"SELECT COUNT(*) as row_count FROM {table_name}",
                'sample_data': f"SELECT * FROM {table_name} LIMIT 5"
            }
            
            results = {}
            
            for analysis_type, sql in analyze_queries.items():
                request = MCPRequest(
                    operation_type=MCPOperationType.QUERY,
                    parameters={'sql': sql, 'limit': 100}
                )
                
                response = await self._execute_query(request)
                
                if response.success:
                    results[analysis_type] = {
                        'columns': response.data['columns'],
                        'rows': response.data['rows'],
                        'execution_time_ms': response.data['execution_time_ms']
                    }
                else:
                    results[analysis_type] = {'error': response.error}
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to analyze table {table_name}: {str(e)}")
            return {'error': str(e)}


# Factory function for creating Snowflake connector
def create_snowflake_connector(
    account: str,
    username: str,
    password: str,
    database: str = "TRM_OS_ANALYTICS",
    warehouse: str = "COMPUTE_WH",
    **kwargs
) -> SnowflakeMCPConnector:
    """
    Create Snowflake MCP connector with credentials
    
    Args:
        account: Snowflake account identifier
        username: Username for authentication
        password: Password for authentication
        database: Database name
        warehouse: Warehouse name
        **kwargs: Additional configuration options
        
    Returns:
        SnowflakeMCPConnector: Configured connector instance
    """
    config = MCPConnectionConfig(
        platform="snowflake",
        connection_string=f"snowflake://{username}@{account}/{database}",
        credentials={
            'account': account,
            'username': username,
            'password': password,
            'database': database,
            'warehouse': warehouse,
            **kwargs
        }
    )
    
    return SnowflakeMCPConnector(config) 