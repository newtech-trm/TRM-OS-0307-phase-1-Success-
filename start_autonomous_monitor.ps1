# AUTONOMOUS RAILWAY MONITOR - POWERSHELL LAUNCHER
# ===============================================
# Complete self-healing Railway monitoring system
# Usage: .\start_autonomous_monitor.ps1

Write-Host "🚀 AUTONOMOUS RAILWAY MONITOR - STARTING COMPLETE SELF-HEALING SYSTEM" -ForegroundColor Green
Write-Host "📋 Features:" -ForegroundColor Cyan
Write-Host "  ✅ Real-time Railway log monitoring" -ForegroundColor White
Write-Host "  ✅ Automatic error detection & classification" -ForegroundColor White
Write-Host "  ✅ Autonomous error fixing" -ForegroundColor White
Write-Host "  ✅ Auto-deployment of fixes" -ForegroundColor White
Write-Host "  ✅ Self-healing & auto-restart" -ForegroundColor White
Write-Host "  ✅ Complete hands-off operation" -ForegroundColor White
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if Railway CLI is available
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ Railway CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Install required dependencies
Write-Host "📦 Installing required dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install asyncio requests

# Set environment variables
$env:PYTHONPATH = $PWD

# Start autonomous monitor
Write-Host "🤖 Starting Autonomous Monitor..." -ForegroundColor Green
Write-Host "⚡ System will now run completely autonomously" -ForegroundColor Yellow
Write-Host "📊 Monitor logs in: autonomous_monitor.log" -ForegroundColor Cyan
Write-Host "🔧 Fix history in: autonomous_monitor_state.json" -ForegroundColor Cyan
Write-Host ""
Write-Host "🛑 Press Ctrl+C to stop the autonomous system" -ForegroundColor Magenta
Write-Host ""

try {
    # Run autonomous monitor
    python run_autonomous_monitor.py
}
catch {
    Write-Host "❌ Autonomous monitor failed: $_" -ForegroundColor Red
    Write-Host "📋 Check logs for details" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🏁 Autonomous Railway Monitor stopped" -ForegroundColor Green 