#!/usr/bin/env python3
"""
AUTONOMOUS RAILWAY LOG MONITOR & AUTO-FIX SYSTEM
===============================================

Hệ thống tự động hoàn chỉnh để:
1. Theo dõi Railway logs real-time
2. Phát hiện và phân loại errors
3. Tự động fix errors mà không cần can thiệp thủ công
4. Deploy fixes tự động
5. Báo cáo kết quả

Philosophy: Complete autonomous operation - "Set it and forget it"
"""

import asyncio
import logging
import json
import re
import time
import subprocess
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass
from enum import Enum
import traceback
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutonomousMonitor")

class ErrorSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class FixStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ErrorPattern:
    """Pattern definition for error detection and auto-fix"""
    pattern: str
    severity: ErrorSeverity
    error_type: str
    description: str
    auto_fix_function: str
    fix_priority: int
    requires_restart: bool = False

@dataclass
class DetectedError:
    """Detected error instance"""
    error_id: str
    timestamp: datetime
    pattern: ErrorPattern
    matched_text: str
    context: Dict[str, Any]
    fix_attempts: int = 0
    fix_status: FixStatus = FixStatus.PENDING

class AutonomousRailwayMonitor:
    """
    Autonomous Railway Log Monitor với Auto-Fix Engine
    
    Complete self-healing system:
    - Continuous log monitoring
    - Automatic error detection
    - Intelligent error classification
    - Autonomous fixing
    - Self-validation
    """
    
    def __init__(self):
        self.logger = logger
        self.is_running = False
        self.detected_errors: Dict[str, DetectedError] = {}
        self.fix_history: List[Dict[str, Any]] = []
        self.last_log_check = datetime.now() - timedelta(minutes=5)
        
        # Railway configuration
        self.railway_project_id = "trm-os-railway"
        self.railway_service_id = "production"
        
        # Error patterns với auto-fix functions
        self.error_patterns = self._initialize_error_patterns()
        
        # Auto-fix engine
        self.auto_fix_engine = AutoFixEngine()
        
        # Statistics
        self.stats = {
            "total_errors_detected": 0,
            "total_errors_fixed": 0,
            "uptime_start": datetime.now(),
            "last_successful_fix": None,
            "fix_success_rate": 0.0
        }
        
        self.logger.info("🤖 Autonomous Railway Monitor initialized - Full auto-healing enabled")
    
    def _initialize_error_patterns(self) -> List[ErrorPattern]:
        """Initialize comprehensive error patterns với auto-fix mappings"""
        return [
            # AgentMetadata validation errors
            ErrorPattern(
                pattern=r"ERROR:AgentTemplateRegistry:Error registering template.*validation errors for AgentMetadata",
                severity=ErrorSeverity.HIGH,
                error_type="agent_metadata_validation",
                description="AgentMetadata validation errors - legacy structure detected",
                auto_fix_function="fix_agent_metadata_validation",
                fix_priority=1
            ),
            
            # Missing required fields
            ErrorPattern(
                pattern=r"Field required.*actor_id|actor_type|semantic_purpose",
                severity=ErrorSeverity.HIGH,
                error_type="missing_required_fields",
                description="Missing required fields in AgentMetadata",
                auto_fix_function="fix_missing_required_fields",
                fix_priority=1
            ),
            
            # Import/Module errors
            ErrorPattern(
                pattern=r"No module named '([^']+)'",
                severity=ErrorSeverity.MEDIUM,
                error_type="missing_module",
                description="Missing Python module",
                auto_fix_function="fix_missing_module",
                fix_priority=2
            ),
            
            # Docker/MCP endpoint issues
            ErrorPattern(
                pattern=r"MCP Conversational endpoints not available.*No module named 'docker'",
                severity=ErrorSeverity.MEDIUM,
                error_type="mcp_docker_missing",
                description="Docker module missing for MCP endpoints",
                auto_fix_function="fix_mcp_docker_dependency",
                fix_priority=2
            ),
            
            # Pydantic warnings
            ErrorPattern(
                pattern=r"'schema_extra' has been renamed to 'json_schema_extra'",
                severity=ErrorSeverity.LOW,
                error_type="pydantic_deprecation",
                description="Pydantic deprecation warnings",
                auto_fix_function="fix_pydantic_deprecation",
                fix_priority=3
            ),
            
            # Database connection errors
            ErrorPattern(
                pattern=r"Connection.*refused|Connection.*timeout|Database.*connection.*failed",
                severity=ErrorSeverity.CRITICAL,
                error_type="database_connection",
                description="Database connection issues",
                auto_fix_function="fix_database_connection",
                fix_priority=1,
                requires_restart=True
            ),
            
            # API endpoint errors
            ErrorPattern(
                pattern=r"404.*Not Found|500.*Internal Server Error|502.*Bad Gateway",
                severity=ErrorSeverity.HIGH,
                error_type="api_endpoint_error",
                description="API endpoint errors",
                auto_fix_function="fix_api_endpoint_errors",
                fix_priority=2
            ),
            
            # Memory/Resource issues
            ErrorPattern(
                pattern=r"MemoryError|Out of memory|Resource.*exhausted",
                severity=ErrorSeverity.CRITICAL,
                error_type="resource_exhaustion",
                description="Memory or resource exhaustion",
                auto_fix_function="fix_resource_exhaustion",
                fix_priority=1,
                requires_restart=True
            )
        ]
    
    async def start_autonomous_monitoring(self):
        """Start complete autonomous monitoring system"""
        self.is_running = True
        self.logger.info("🚀 Starting Autonomous Railway Monitor - Full Auto-Healing Mode")
        
        # Start monitoring tasks
        tasks = [
            self._continuous_log_monitor(),
            self._autonomous_fix_engine(),
            self._health_check_loop(),
            self._statistics_reporter(),
            self._self_diagnostic_loop()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"❌ Autonomous monitor crashed: {e}")
            await self._emergency_recovery()
    
    async def _continuous_log_monitor(self):
        """Continuously monitor Railway logs"""
        self.logger.info("📡 Starting continuous log monitoring")
        
        while self.is_running:
            try:
                # Get recent logs
                logs = await self._fetch_railway_logs()
                
                if logs:
                    # Process logs for errors
                    new_errors = await self._analyze_logs_for_errors(logs)
                    
                    if new_errors:
                        self.logger.warning(f"🔍 Detected {len(new_errors)} new errors")
                        for error in new_errors:
                            self.detected_errors[error.error_id] = error
                            self.stats["total_errors_detected"] += 1
                
                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Error in log monitoring: {e}")
                await asyncio.sleep(60)  # Back off on error
    
    async def _fetch_railway_logs(self) -> List[str]:
        """Fetch recent Railway logs"""
        try:
            # Get logs from last check time
            time_filter = self.last_log_check.strftime("%Y-%m-%d %H:%M:%S")
            
            # Railway CLI command to get logs
            cmd = [
                "railway", "logs", 
                "--service", self.railway_service_id,
                "--since", "5m",  # Last 5 minutes
                "--json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                log_lines = result.stdout.strip().split('\n')
                self.last_log_check = datetime.now()
                return [line for line in log_lines if line.strip()]
            else:
                self.logger.warning(f"⚠️ Railway CLI returned error: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            self.logger.warning("⚠️ Railway logs fetch timeout")
            return []
        except Exception as e:
            self.logger.error(f"❌ Error fetching Railway logs: {e}")
            return []
    
    async def _analyze_logs_for_errors(self, logs: List[str]) -> List[DetectedError]:
        """Analyze logs và detect errors using patterns"""
        detected_errors = []
        
        for log_line in logs:
            for pattern in self.error_patterns:
                match = re.search(pattern.pattern, log_line, re.IGNORECASE)
                if match:
                    error_id = f"{pattern.error_type}_{int(time.time())}_{len(detected_errors)}"
                    
                    error = DetectedError(
                        error_id=error_id,
                        timestamp=datetime.now(),
                        pattern=pattern,
                        matched_text=log_line,
                        context={
                            "full_log": log_line,
                            "match_groups": match.groups() if match.groups() else [],
                            "source": "railway_logs"
                        }
                    )
                    
                    detected_errors.append(error)
                    self.logger.warning(f"🔍 Detected {pattern.error_type}: {log_line[:100]}...")
        
        return detected_errors
    
    async def _autonomous_fix_engine(self):
        """Autonomous engine để fix errors tự động"""
        self.logger.info("🤖 Starting Autonomous Fix Engine")
        
        while self.is_running:
            try:
                # Get pending errors sorted by priority
                pending_errors = [
                    error for error in self.detected_errors.values() 
                    if error.fix_status == FixStatus.PENDING
                ]
                
                if pending_errors:
                    # Sort by priority (lower number = higher priority)
                    pending_errors.sort(key=lambda x: x.pattern.fix_priority)
                    
                    for error in pending_errors[:3]:  # Fix up to 3 errors per cycle
                        await self._execute_autonomous_fix(error)
                
                await asyncio.sleep(45)  # Check every 45 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Error in autonomous fix engine: {e}")
                await asyncio.sleep(60)
    
    async def _execute_autonomous_fix(self, error: DetectedError):
        """Execute autonomous fix for detected error"""
        self.logger.info(f"🔧 Executing autonomous fix for {error.pattern.error_type}")
        
        error.fix_status = FixStatus.IN_PROGRESS
        error.fix_attempts += 1
        
        try:
            # Get fix function
            fix_function = getattr(self.auto_fix_engine, error.pattern.auto_fix_function, None)
            
            if not fix_function:
                self.logger.error(f"❌ Fix function {error.pattern.auto_fix_function} not found")
                error.fix_status = FixStatus.FAILED
                return
            
            # Execute fix
            fix_result = await fix_function(error)
            
            if fix_result.get("success", False):
                error.fix_status = FixStatus.COMPLETED
                self.stats["total_errors_fixed"] += 1
                self.stats["last_successful_fix"] = datetime.now()
                
                # Log fix result
                self.fix_history.append({
                    "error_id": error.error_id,
                    "error_type": error.pattern.error_type,
                    "fix_timestamp": datetime.now().isoformat(),
                    "fix_result": fix_result,
                    "attempts": error.fix_attempts
                })
                
                self.logger.info(f"✅ Successfully fixed {error.pattern.error_type}")
                
                # Deploy fix if needed
                if fix_result.get("requires_deployment", False):
                    await self._autonomous_deploy()
                    
                # Restart if required
                if error.pattern.requires_restart:
                    await self._request_service_restart()
                
            else:
                error.fix_status = FixStatus.FAILED
                self.logger.error(f"❌ Failed to fix {error.pattern.error_type}: {fix_result.get('error')}")
                
        except Exception as e:
            error.fix_status = FixStatus.FAILED
            self.logger.error(f"❌ Exception during fix execution: {e}")
            self.logger.error(traceback.format_exc())
    
    async def _autonomous_deploy(self):
        """Autonomous deployment of fixes"""
        self.logger.info("🚀 Executing autonomous deployment")
        
        try:
            # Git add all changes
            subprocess.run(["git", "add", "."], cwd=".", check=True)
            
            # Commit with timestamp
            commit_msg = f"🤖 AUTONOMOUS FIX: Auto-fixed detected errors at {datetime.now().isoformat()}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=".", check=True)
            
            # Push changes
            subprocess.run(["git", "push"], cwd=".", check=True)
            
            self.logger.info("✅ Autonomous deployment completed")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Autonomous deployment failed: {e}")
    
    async def _request_service_restart(self):
        """Request Railway service restart"""
        self.logger.info("🔄 Requesting service restart")
        
        try:
            # Railway CLI restart command
            subprocess.run(["railway", "service", "restart"], check=True, timeout=60)
            self.logger.info("✅ Service restart requested")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to restart service: {e}")
    
    async def _health_check_loop(self):
        """Continuous health checking"""
        while self.is_running:
            try:
                # Check system health
                health_status = await self._perform_health_check()
                
                if not health_status.get("healthy", False):
                    self.logger.warning(f"⚠️ Health check failed: {health_status}")
                    # Auto-remediation if possible
                    await self._auto_remediate_health_issues(health_status)
                
                await asyncio.sleep(300)  # Every 5 minutes
                
            except Exception as e:
                self.logger.error(f"❌ Health check error: {e}")
                await asyncio.sleep(300)
    
    async def _perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        try:
            # Check service accessibility
            health_url = "https://trmsongnhanh.up.railway.app/health"  # Assuming health endpoint
            response = requests.get(health_url, timeout=10)
            
            return {
                "healthy": response.status_code == 200,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _auto_remediate_health_issues(self, health_status: Dict[str, Any]):
        """Auto-remediate health issues"""
        self.logger.info("🔧 Attempting auto-remediation of health issues")
        
        # Simple remediation strategies
        if health_status.get("status_code") in [502, 503, 504]:
            # Service may be down - request restart
            await self._request_service_restart()
    
    async def _statistics_reporter(self):
        """Report statistics periodically"""
        while self.is_running:
            try:
                # Calculate fix success rate
                if self.stats["total_errors_detected"] > 0:
                    self.stats["fix_success_rate"] = (
                        self.stats["total_errors_fixed"] / self.stats["total_errors_detected"]
                    ) * 100
                
                uptime = datetime.now() - self.stats["uptime_start"]
                
                self.logger.info(
                    f"📊 AUTONOMOUS MONITOR STATS - "
                    f"Uptime: {uptime}, "
                    f"Errors Detected: {self.stats['total_errors_detected']}, "
                    f"Errors Fixed: {self.stats['total_errors_fixed']}, "
                    f"Success Rate: {self.stats['fix_success_rate']:.1f}%"
                )
                
                await asyncio.sleep(3600)  # Report every hour
                
            except Exception as e:
                self.logger.error(f"❌ Statistics reporting error: {e}")
                await asyncio.sleep(3600)
    
    async def _self_diagnostic_loop(self):
        """Self-diagnostic và self-healing for monitor itself"""
        while self.is_running:
            try:
                # Check if monitor is functioning properly
                recent_activity = datetime.now() - timedelta(minutes=10)
                
                # Check if we've detected any activity recently
                if self.last_log_check < recent_activity:
                    self.logger.warning("⚠️ No recent log activity - potential monitor issue")
                    # Reset log check time
                    self.last_log_check = datetime.now() - timedelta(minutes=1)
                
                await asyncio.sleep(600)  # Self-check every 10 minutes
                
            except Exception as e:
                self.logger.error(f"❌ Self-diagnostic error: {e}")
                await asyncio.sleep(600)
    
    async def _emergency_recovery(self):
        """Emergency recovery procedures"""
        self.logger.critical("🆘 Initiating emergency recovery")
        
        try:
            # Log current state
            self.logger.critical(f"Monitor state: {len(self.detected_errors)} detected errors")
            
            # Try to save state
            await self._save_monitor_state()
            
            # Attempt automatic restart
            self.logger.critical("🔄 Attempting automatic restart")
            await asyncio.sleep(5)
            
            # Restart monitoring
            self.is_running = True
            await self.start_autonomous_monitoring()
            
        except Exception as e:
            self.logger.critical(f"💀 Emergency recovery failed: {e}")
    
    async def _save_monitor_state(self):
        """Save current monitor state"""
        try:
            state = {
                "timestamp": datetime.now().isoformat(),
                "detected_errors": len(self.detected_errors),
                "stats": self.stats,
                "recent_fixes": self.fix_history[-10:]  # Last 10 fixes
            }
            
            with open("autonomous_monitor_state.json", "w") as f:
                json.dump(state, f, indent=2, default=str)
                
            self.logger.info("💾 Monitor state saved")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save monitor state: {e}")


class AutoFixEngine:
    """
    Autonomous Fix Engine - Implements actual fix functions
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AutoFixEngine")
    
    async def fix_agent_metadata_validation(self, error: DetectedError) -> Dict[str, Any]:
        """Fix AgentMetadata validation errors automatically"""
        self.logger.info("🔧 Fixing AgentMetadata validation errors")
        
        try:
            # Search for files với legacy AgentMetadata creation
            legacy_patterns = [
                r'AgentMetadata\(\s*name\s*=',
                r'agent_type\s*=\s*["\']',
                r'description\s*=\s*["\'].*["\'],',
                r'status\s*=\s*["\']active["\']'
            ]
            
            files_to_fix = []
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            for pattern in legacy_patterns:
                                if re.search(pattern, content):
                                    if file_path not in files_to_fix:
                                        files_to_fix.append(file_path)
                        except:
                            continue
            
            if files_to_fix:
                self.logger.info(f"🔍 Found {len(files_to_fix)} files to fix")
                
                fixes_applied = 0
                for file_path in files_to_fix:
                    if await self._fix_file_metadata(file_path):
                        fixes_applied += 1
                
                return {
                    "success": True,
                    "files_fixed": fixes_applied,
                    "requires_deployment": fixes_applied > 0,
                    "message": f"Fixed AgentMetadata in {fixes_applied} files"
                }
            else:
                return {
                    "success": True,
                    "files_fixed": 0,
                    "requires_deployment": False,
                    "message": "No legacy AgentMetadata patterns found"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fix AgentMetadata validation"
            }
    
    async def _fix_file_metadata(self, file_path: str) -> bool:
        """Fix AgentMetadata in specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix legacy AgentMetadata patterns
            replacements = [
                # Replace legacy metadata creation
                (
                    r'AgentMetadata\(\s*name\s*=\s*([^,]+),\s*agent_type\s*=\s*([^,]+),\s*description\s*=\s*([^,]+),?\s*capabilities\s*=\s*([^,]+)?,?\s*status\s*=\s*[^,]+,?\s*version\s*=\s*[^)]+\)',
                    r'AgentMetadata(\n                actor_id=agent_id,\n                actor_type=f"AGE_AGENT_{agent_id.upper() if agent_id else \'UNKNOWN\'}",\n                semantic_purpose=f"AGE Actor - {\\3}",\n                capabilities=\\4 if \\4 else [],\n                strategic_context={"creation_date": datetime.now().isoformat(), "age_integration": True},\n                performance_metrics={"initialization_timestamp": datetime.now().timestamp()}\n            )'
                )
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"✅ Fixed metadata in {file_path}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Error fixing {file_path}: {e}")
            return False
    
    async def fix_missing_required_fields(self, error: DetectedError) -> Dict[str, Any]:
        """Fix missing required fields in AgentMetadata"""
        return await self.fix_agent_metadata_validation(error)
    
    async def fix_missing_module(self, error: DetectedError) -> Dict[str, Any]:
        """Fix missing Python modules automatically"""
        try:
            # Extract module name from error
            match = re.search(r"No module named '([^']+)'", error.matched_text)
            if not match:
                return {"success": False, "error": "Could not extract module name"}
            
            module_name = match.group(1)
            self.logger.info(f"🔧 Installing missing module: {module_name}")
            
            # Install module
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", module_name
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "module_installed": module_name,
                    "requires_deployment": False,
                    "message": f"Successfully installed {module_name}"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "message": f"Failed to install {module_name}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fix missing module"
            }
    
    async def fix_mcp_docker_dependency(self, error: DetectedError) -> Dict[str, Any]:
        """Fix MCP Docker dependency issues"""
        try:
            # Install docker module
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "docker>=7.0.0"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "requires_deployment": False,
                    "message": "Successfully installed docker module for MCP endpoints"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "message": "Failed to install docker module"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fix MCP docker dependency"
            }
    
    async def fix_pydantic_deprecation(self, error: DetectedError) -> Dict[str, Any]:
        """Fix Pydantic deprecation warnings"""
        try:
            # Search for schema_extra usage
            files_fixed = 0
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if 'schema_extra' in content:
                                content = content.replace('schema_extra', 'json_schema_extra')
                                
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                
                                files_fixed += 1
                        except:
                            continue
            
            return {
                "success": True,
                "files_fixed": files_fixed,
                "requires_deployment": files_fixed > 0,
                "message": f"Fixed Pydantic deprecation in {files_fixed} files"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to fix Pydantic deprecation"
            }
    
    async def fix_database_connection(self, error: DetectedError) -> Dict[str, Any]:
        """Fix database connection issues"""
        return {
            "success": False,
            "error": "Database connection issues require manual intervention",
            "message": "Cannot automatically fix database connectivity"
        }
    
    async def fix_api_endpoint_errors(self, error: DetectedError) -> Dict[str, Any]:
        """Fix API endpoint errors"""
        return {
            "success": False,
            "error": "API endpoint errors require investigation",
            "message": "Cannot automatically fix API endpoint issues"
        }
    
    async def fix_resource_exhaustion(self, error: DetectedError) -> Dict[str, Any]:
        """Fix resource exhaustion issues"""
        return {
            "success": False,
            "error": "Resource exhaustion requires scaling or optimization",
            "message": "Cannot automatically fix resource issues"
        }


async def main():
    """Main function to run autonomous monitor"""
    logger.info("🚀 Starting Autonomous Railway Monitor System")
    
    monitor = AutonomousRailwayMonitor()
    
    try:
        await monitor.start_autonomous_monitoring()
    except KeyboardInterrupt:
        logger.info("⏹️ Autonomous monitor stopped by user")
    except Exception as e:
        logger.critical(f"💀 Autonomous monitor crashed: {e}")
        logger.critical(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main()) 