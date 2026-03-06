# ============================================================
# UNASAT Campus Support Chatbot — Automated Setup (Windows)
# ============================================================
# Usage: Right-click > Run with PowerShell
#        OR: powershell -ExecutionPolicy Bypass -File setup.ps1
# ============================================================

Write-Host ""
Write-Host "======================================================" -ForegroundColor Green
Write-Host "  UNASAT Campus Support Chatbot — Setup" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""

# ── Step 1: Check Docker ─────────────────────────────────────
Write-Host "[1/5] Checking Docker..." -ForegroundColor Cyan
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Download Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}
Write-Host "      Docker found." -ForegroundColor Green

# ── Step 2: Check Docker is running ──────────────────────────
Write-Host "[2/5] Checking Docker daemon..." -ForegroundColor Cyan
$dockerStatus = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}
Write-Host "      Docker is running." -ForegroundColor Green

# ── Step 3: Create .env if it doesn't exist ──────────────────
Write-Host "[3/5] Setting up environment file..." -ForegroundColor Cyan
$envFile = "backend\.env"
$envExample = "backend\.env.example"

if (Test-Path $envFile) {
    Write-Host "      backend\.env already exists, skipping." -ForegroundColor Yellow
} else {
    if (-not (Test-Path $envExample)) {
        Write-Host "ERROR: backend\.env.example not found." -ForegroundColor Red
        exit 1
    }
    Copy-Item $envExample $envFile
    Write-Host "      Created backend\.env from example." -ForegroundColor Green
    Write-Host ""
    Write-Host "  ACTION REQUIRED:" -ForegroundColor Yellow
    Write-Host "  Open backend\.env and fill in your GROQ_API_KEY." -ForegroundColor Yellow
    Write-Host "  Get a free key at: https://console.groq.com" -ForegroundColor Yellow
    Write-Host ""
    $confirm = Read-Host "  Press ENTER when you have added your API key, or type 'skip' to continue anyway"
}

# ── Step 4: Verify GROQ_API_KEY is set ───────────────────────
Write-Host "[4/5] Verifying API key..." -ForegroundColor Cyan
$envContent = Get-Content $envFile -Raw
if ($envContent -match "GROQ_API_KEY=your_groq_api_key_here" -or $envContent -match "GROQ_API_KEY=$") {
    Write-Host "WARNING: GROQ_API_KEY appears to be empty or not set." -ForegroundColor Yellow
    Write-Host "         The chatbot will start but LLM fallback won't work." -ForegroundColor Yellow
} else {
    Write-Host "      API key found." -ForegroundColor Green
}

# ── Step 5: Build and start ───────────────────────────────────
Write-Host "[5/5] Building and starting containers..." -ForegroundColor Cyan
Write-Host "      This may take 5-10 minutes on first run." -ForegroundColor Gray
Write-Host ""

docker compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Docker Compose failed. Check the output above." -ForegroundColor Red
    exit 1
}

# ── Done ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "======================================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Chatbot:         http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Admin dashboard: http://localhost:3000/admin" -ForegroundColor Cyan
Write-Host "  Backend API:     http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API docs:        http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  To stop:  docker compose down" -ForegroundColor Gray
Write-Host "  To reset: docker compose down -v" -ForegroundColor Gray
Write-Host ""