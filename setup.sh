#!/bin/bash
echo "🚀 Lancaster Finance Tracker Setup"

# Create & activate venv
python -m venv lancaster-finance-venv
source lancaster-finance-venv/Scripts/activate # On Windows: lancaster-finance-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
echo "Virtual environment ready!"

# Setup env file
cp .env.example .env

echo "✅ Setup complete!"
echo "📝 Edit .env → Add your OpenAI key (https://platform.openai.com/api-keys)"
echo "🎯 Run: uvicorn app.main:app --reload --port 8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "💚 Test it:"
echo "curl http://localhost:8000/health"