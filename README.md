# Lancaster Finance Tracker

AI-powered expense analyser for Lancaster students. Submit expenses; get categorised spending, risk alerts, and Lancaster-specific financial advice.

## What it does
Students submit recent expenses (date/amount/description). AI:
- Categorises spending (food/rent/transport)
- Flags risky patterns (takeaways>groceries)
- Detects bursary eligibility signals
- Links ASK/LUSU money advice
- Suggests student savings (campus store discounts, bulk cooking)

Improves journey by preventing debt, maximising bursaries, building financial literacy.

## One-Command Setup

### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
```

### Windows (Git Bash/PowerShell)
```bash
bash setup.sh
```
**Expected output:**
```bash
Choose ONE option:
 1. DEMO MODE: export MOCK_MODE=true && uvicorn app.main:app --reload
 2. REAL AI: Edit .env → uvicorn app.main:app --reload --port 8000
```

## Test in Browser

1. **Start server:**
```bash
export MOCK_MODE=true && uvicorn app.main:app --reload
```
2. **Open:** http://localhost:8000/docs

3. **Click `/feature` → `Try it out` → `Execute`**

## Test API from terminal

**Health check:**
```bash
curl http://localhost:8000/health
```

**Demo analysis (without OpenAI key):**
```bash
curl -X POST http://localhost:8000/feature
-H "Content-Type: application/json"
-d '{"student_id":"s123456","expenses":[{"date":"2025-11-25","amount":12.50,"description":"coffee","merchant":"LU Costa Coffee"}]}'
```

**Interactive docs:** http://localhost:8000/docs
