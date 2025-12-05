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
echo "2. OLLAMA AI: ollama.com -> ollama pull llama3.2 -> edit .env -> restart"
echo ""
echo "3. OPENAI AI: platform.openai.com/api-keys -> edit .env -> restart"
echo ""
echo "http://localhost:8000/docs" -> /feature -> Execute
echo ""
read -p "Press Enter when ready..."
