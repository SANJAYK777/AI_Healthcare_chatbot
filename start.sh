#!/bin/bash
# AI Healthcare Chatbot - Quick Start Script
# Usage: bash start.sh

set -e

echo "🏥 AI Healthcare Chatbot Platform"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}[1/6]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Install from: https://www.python.org"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check Node.js
echo -e "${YELLOW}[2/6]${NC} Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js not found${NC}"
    echo "Install from: https://nodejs.org"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Setup Backend
echo -e "${YELLOW}[3/6]${NC} Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Edit .env with your API keys${NC}"
fi

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

cd ..
echo -e "${GREEN}✓ Backend ready${NC}"

# Setup Frontend
echo -e "${YELLOW}[4/6]${NC} Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install -q
fi

cd ..
echo -e "${GREEN}✓ Frontend ready${NC}"

# Display instructions
echo ""
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo ""
echo "To start the platform:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to:${NC}"
echo "  1. Add API keys to backend/.env"
echo "  2. Check MongoDB connection string"
echo "  3. Generate encryption key (see SETUP_GUIDE.md)"
echo ""
echo "📚 Documentation: Check SETUP_GUIDE.md for detailed instructions"
echo "🚀 Deploy guide: Check DEPLOYMENT.md for production deployment"
echo ""
