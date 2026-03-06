#!/bin/bash
# ============================================================
# UNASAT Campus Support Chatbot — Automated Setup (Linux/Mac)
# ============================================================
# Usage: chmod +x setup.sh && ./setup.sh
# ============================================================

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

echo ""
echo -e "${GREEN}======================================================"
echo -e "  UNASAT Campus Support Chatbot — Setup"
echo -e "======================================================${NC}"
echo ""

# ── Step 1: Check Docker ─────────────────────────────────────
echo -e "${CYAN}[1/5] Checking Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed.${NC}"
    echo -e "${YELLOW}Download from: https://www.docker.com/products/docker-desktop/${NC}"
    exit 1
fi
echo -e "${GREEN}      Docker found.${NC}"

# ── Step 2: Check Docker is running ──────────────────────────
echo -e "${CYAN}[2/5] Checking Docker daemon...${NC}"
if ! docker info &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not running. Please start Docker Desktop first.${NC}"
    exit 1
fi
echo -e "${GREEN}      Docker is running.${NC}"

# ── Step 3: Create .env if it doesn't exist ──────────────────
echo -e "${CYAN}[3/5] Setting up environment file...${NC}"
ENV_FILE="backend/.env"
ENV_EXAMPLE="backend/.env.example"

if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}      backend/.env already exists, skipping.${NC}"
else
    if [ ! -f "$ENV_EXAMPLE" ]; then
        echo -e "${RED}ERROR: backend/.env.example not found.${NC}"
        exit 1
    fi
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo -e "${GREEN}      Created backend/.env from example.${NC}"
    echo ""
    echo -e "${YELLOW}  ACTION REQUIRED:"
    echo -e "  Open backend/.env and fill in your GROQ_API_KEY."
    echo -e "  Get a free key at: https://console.groq.com${NC}"
    echo ""
    read -p "  Press ENTER when you have added your API key..."
fi

# ── Step 4: Verify GROQ_API_KEY is set ───────────────────────
echo -e "${CYAN}[4/5] Verifying API key...${NC}"
if grep -q "GROQ_API_KEY=your_groq_api_key_here\|GROQ_API_KEY=$" "$ENV_FILE"; then
    echo -e "${YELLOW}WARNING: GROQ_API_KEY appears empty. LLM fallback won't work.${NC}"
else
    echo -e "${GREEN}      API key found.${NC}"
fi

# ── Step 5: Build and start ───────────────────────────────────
echo -e "${CYAN}[5/5] Building and starting containers...${NC}"
echo -e "${GRAY}      This may take 5-10 minutes on first run.${NC}"
echo ""

docker compose up --build -d

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Docker Compose failed. Check the output above.${NC}"
    exit 1
fi

# ── Done ─────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}======================================================"
echo -e "  Setup complete!"
echo -e "======================================================${NC}"
echo ""
echo -e "${CYAN}  Chatbot:         http://localhost:3000"
echo -e "  Admin dashboard: http://localhost:3000/admin"
echo -e "  Backend API:     http://localhost:8000"
echo -e "  API docs:        http://localhost:8000/docs${NC}"
echo ""
echo -e "${GRAY}  To stop:  docker compose down"
echo -e "  To reset: docker compose down -v${NC}"
echo ""