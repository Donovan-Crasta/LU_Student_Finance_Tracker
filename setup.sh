#!/bin/bash
echo "🚀 Lancaster Finance Tracker Setup"

python3 -m venv lancaster-finance-venv
source lancaster-finance-venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

echo "Setup complete!"
echo ""
echo "Choose ONE option:"
echo ""
echo "1. DEMO MODE (no key needed):"
echo " export MOCK_MODE=true && uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. REAL AI: Edit .env -> uvicorn app.main:app --reload --port 8000"
echo ""
echo "http://localhost:8000/docs"
read -p "Press Enter when ready..."