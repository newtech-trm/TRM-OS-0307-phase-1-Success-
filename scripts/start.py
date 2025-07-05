#!/usr/bin/env python3
"""
TRM-OS Production Startup Script
Handles PORT environment variable for Railway deployment
"""
import os
import sys
import subprocess

def main():
    # Get PORT from environment, default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Validate port is numeric
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError(f"Port {port_int} is out of valid range")
    except ValueError as e:
        print(f"Invalid PORT value '{port}': {e}")
        print("Using default port 8000")
        port = '8000'
    
    print(f"🚀 Starting TRM-OS API on port {port}")
    
    # Log environment for debugging
    env_vars = {k: v for k, v in os.environ.items() 
                if k.startswith(('PORT', 'PYTHONPATH', 'NEO4J_', 'DATABASE_'))}
    print(f"📋 Environment: {env_vars}")
    
    # Prepare uvicorn command
    cmd = [
        sys.executable, '-m', 'uvicorn', 
        'trm_api.main:app',
        '--host', '0.0.0.0',
        '--port', port,
        '--workers', '4',
        '--log-level', 'info',
        '--access-log'
    ]
    
    print(f"🔧 Command: {' '.join(cmd)}")
    
    # Execute uvicorn
    try:
        os.execvp(sys.executable, cmd)
    except Exception as e:
        print(f"❌ Failed to start uvicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 