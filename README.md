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
```bash
uvicorn app.main:app --reload --port 8000
```

**Health check:**
```bash
curl http://localhost:8000/health
```
**Output**
```bash
{"status":"ok","service":"lancaster-finance-tracker"}
```

**Demo Analysis**
```bash
curl -X POST http://localhost:8000/feature -H 'Content-Type: application/json' -d '{"student_id": "s1", "expenses": [{"date":"2025-11-25","amount": 120,"description": "shopping","merchant": "M&S"},
{"date": "2025-11-27","amount": 80,"description": "food","merchant": "Sultan"},
{"date": "2025-11-26","amount": 12.50,"description": "ice skating","merchant": "Dalton"}],
"income_sources": ["part-time TA"]
}'
```

**Sample Output**
```bash
{"summary":{"total_spent":212.5,"avg_daily_spend":70.83,"risk_level":"high","risk_factors":["Total spending: £212.50"]},"categorisation":{"food":"80.00","transport":0,"rent":0,"utilities":0,"entertainment":0,"groceries":"120.00","miscellaneous":"12.50"},"alerts":[{"type":"high_spend","message":"Weekly spending exceeds £200. Review ASK money advice.","url":"https://portal.lancaster.ac.uk/ask/money/"}],"advice":["Track spending weekly via this API","Batch cook to save £20/week","Use campus store discounts"]}
```

**Interactive docs:** http://localhost:8000/docs
