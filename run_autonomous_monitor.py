#!/usr/bin/env python3
"""
AUTONOMOUS RAILWAY MONITOR LAUNCHER
==================================

Launcher script để chạy autonomous monitoring system với:
- Auto-restart capabilities
- Error recovery
- Background operation
- Complete self-healing

Usage: python run_autonomous_monitor.py
"""

import asyncio
import subprocess
import sys
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - LAUNCHER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_launcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutonomousLauncher")

class AutonomousLauncher:
    """Launcher với auto-restart và error recovery"""
    
    def __init__(self):
        self.max_restarts = 10
        self.restart_count = 0
        self.is_running = True
        
    async def run_with_auto_restart(self):
        """Run autonomous monitor với auto-restart"""
        logger.info("🚀 Starting Autonomous Railway Monitor with Auto-Restart")
        
        while self.is_running and self.restart_count < self.max_restarts:
            try:
                # Import và run autonomous monitor
                from scripts.autonomous_railway_monitor import main as monitor_main
                
                logger.info(f"🔄 Starting monitor (Attempt {self.restart_count + 1})")
                await monitor_main()
                
            except KeyboardInterrupt:
                logger.info("⏹️ Shutdown requested by user")
                self.is_running = False
                break
                
            except Exception as e:
                self.restart_count += 1
                logger.error(f"❌ Monitor crashed (Attempt {self.restart_count}): {e}")
                
                if self.restart_count < self.max_restarts:
                    wait_time = min(60 * self.restart_count, 300)  # Max 5 minutes
                    logger.info(f"🔄 Restarting in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.critical("💀 Max restart attempts reached. Stopping.")
                    break
        
        logger.info("🏁 Autonomous launcher finished")

async def main():
    """Main launcher function"""
    launcher = AutonomousLauncher()
    await launcher.run_with_auto_restart()

if __name__ == "__main__":
    # Check if running on Windows/PowerShell
    logger.info("🎯 Autonomous Railway Monitor - Complete Self-Healing System")
    logger.info("📋 Features: Auto-detection, Auto-fix, Auto-deploy, Auto-restart")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"💀 Launcher failed: {e}")
        sys.exit(1) 