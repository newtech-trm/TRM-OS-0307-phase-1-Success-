#!/usr/bin/env python3
"""
Railway startup script để handle PORT environment variable
"""
import os
import subprocess
import sys

def main():
    # Get PORT from environment or default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Build uvicorn command
    cmd = [
        'uvicorn',
        'trm_api.main:app',
        '--host', '0.0.0.0',
        '--port', port,
        '--workers', '4'
    ]
    
    print(f"🚀 Starting TRM-OS API on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute uvicorn
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 