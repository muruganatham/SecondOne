# Backend Quick Start Script
# This script helps you start the backend server quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Application Backend - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the correct directory
$currentDir = Get-Location
if ($currentDir.Path -notlike "*backend*") {
    Write-Host "⚠️  Warning: You might not be in the backend directory" -ForegroundColor Yellow
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    Write-Host ""
}

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8 or higher" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if virtual environment exists
Write-Host "🔍 Checking for virtual environment..." -ForegroundColor Green
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "⚠️  No virtual environment found" -ForegroundColor Yellow
    $createVenv = Read-Host "Would you like to create one? (y/n)"
    if ($createVenv -eq "y") {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
        Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
        & "venv\Scripts\Activate.ps1"
    }
}
Write-Host ""

# Check if requirements are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Green
try {
    python -c "import fastapi" 2>$null
    Write-Host "✅ Dependencies appear to be installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Dependencies not found" -ForegroundColor Yellow
    $installDeps = Read-Host "Would you like to install them now? (y/n)"
    if ($installDeps -eq "y") {
        Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    }
}
Write-Host ""

# Check if .env file exists
Write-Host "🔍 Checking .env configuration..." -ForegroundColor Green
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Please create a .env file with your database credentials" -ForegroundColor Yellow
}
Write-Host ""

# Check if MySQL is running
Write-Host "🔍 Checking MySQL connection..." -ForegroundColor Green
try {
    $mysqlCheck = mysql -u root -p"Varun1121@#" -e "SELECT 1" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ MySQL connection successful" -ForegroundColor Green
    } else {
        Write-Host "⚠️  MySQL connection failed" -ForegroundColor Yellow
        Write-Host "Please ensure MySQL is running and credentials are correct" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not check MySQL connection" -ForegroundColor Yellow
}
Write-Host ""

# Start the server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Yellow
Write-Host "  - Local:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Network: http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "  - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
