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

## Quick Setup

## 1. Create & activate virtual environment

### Linux/macOS
```bash
python3 -m venv lancaster-finance-venv
source lancaster-finance-venv/bin/activate
```

### Windows (PowerShell)
```bash
python -m venv lancaster-finance-venv
.\lancaster-finance-venv\Scripts\Activate.ps1
```

### Windows (Git Bash)
```bash
python -m venv lancaster-finance-venv
source lancaster-finance-venv/Scripts/activate
```

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Configure AI:
### Ollama (local AI, no key required)

*Install Ollama*: https://ollama.com/download

```bash
ollama pull llama3.2    # ~2GB, needed just the first time
```

### OpenAI (Requires paid key)
**Edit .env**
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-proj-your-key-here
```

## 4. Run API
```bash
uvicorn app.main:app --reload --port 8000
```

## 5. Test in Browser

**Open:** http://localhost:8000/docs

**Click `/feature` → `Try it out` → `Execute`**

## 6. Test API from terminal

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
## 7. Testing
```bash
pytest tests/ -v
```

**Interactive docs:** http://localhost:8000/docs
