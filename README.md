# Lancaster Finance Tracker

AI-powered expense analyzer for Lancaster students. Submit expenses; get categorized spending, risk alerts, and Lancaster-specific financial advice.

## What it does
Students submit recent expenses (date/amount/description). AI:
- Categorizes spending (food/rent/transport)
- Flags risky patterns (takeaways>groceries)
- Detects bursary eligibility signals
- Links ASK/LUSU money advice
- Suggests student savings (campus store discounts, bulk cooking)

Improves journey by preventing debt, maximizing bursaries, building financial literacy.

## Quick Start (Virtual Environment - Required)

### Developer/Tester Instructions

1. Clone and Create Virtual Environment
```bash
git clone <repo> && cd lancaster-finance-tracker
python -m venv lancaster-finance-venv
```

2. Activate (choose your OS)
Windows:
```bash
lancaster-finance-venv\Scripts\activate
```

macOS/Linux:
```bash
source lancaster-finance-venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Add your OpenAPI key
```bash
cp .env.example .env
```
Edit .env -> Paste your sk-proj-... key

5. Run
uvicorn app.main:app --reload --port 8000

**Test immediately:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/feature -H "Content-Type: application/json" -d '{"student_id": "test", "expenses":[{"date":"2025-11-25", "amount": 12.50, "description": "coffee", "merchant": "LU costa"}]}'
```