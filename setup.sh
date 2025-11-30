#!/bin/bash
echo "Lancaster Finance Tracker Setup"

# Create & activate venv
python -m venv lancaster-finance-venv
source lancaster-finance-venv/Scripts/activate # On Windows: lancaster-finance-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
echo "Virtual environment ready!"

# Setup env file
cp .env.example .env

echo "Setup complete!"
uvicorn app.main:app --reload --port 8000