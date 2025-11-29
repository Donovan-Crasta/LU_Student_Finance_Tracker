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

## 🚀 One-Command Setup

### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

### Windows (Git Bash/PowerShell)
```bash
bash setup.sh
```

**That's it!** Edit `.env` with your OpenAI key, then:
```bash
uvicorn app.main:app --reload --port 8000
```

**Test immediately:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/feature -H "Content-Type: application/json" -d '{"student_id": "test", "expenses":[{"date":"2025-11-25", "amount": 12.50, "description": "coffee", "merchant": "LU costa"}]}'
```