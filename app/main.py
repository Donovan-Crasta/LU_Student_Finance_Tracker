import logging
import json
import os
from typing import List
from datetime import date
from decimal import Decimal

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("lancaster-finance-tracker")

class Expense(BaseModel):
    date: date
    amount: Decimal = Field(..., gt=0)
    description: str
    merchant: str

class FinanceRequest(BaseModel):
    student_id: str
    expenses: List[Expense] = Field(..., min_items=1)
    income_sources: List[str] = Field(default_factory=list)

class CategorySummary(BaseModel):
    food: Decimal = 0
    transport: Decimal = 0
    rent: Decimal = 0
    utilities: Decimal = 0
    entertainment: Decimal = 0
    groceries: Decimal = 0
    miscellaneous: Decimal = 0

class Alert(BaseModel):
    type: str
    message: str
    url: str = None

class FinanceResponse(BaseModel):
    summary: dict
    categorisation: CategorySummary
    alerts: List[Alert]
    advice: List[str]

app = FastAPI(
    title="Lancaster Student Finance Tracker",
    description="AI-powered finance tracking and advice for Lancaster University students.",
    version="1.0.0",
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "lancaster-finance-tracker"}

async def call_ai_model(prompt: str) -> str:
    """Call OpenAI-compatible chat completion endpoint."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer{api_key}"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": (
                "You are a finance advisor for Lancaster University students. "
                "Analyse their spending patterns and provide actionable advice."
                "Return ONLY valid JSON matching this exact schema:\n"
                "{\n"
                '"risk_level": "low|medium|high",\n'
                '"risk_factors": ["string"],\n'
                '"total_spent": number,\n'
                '"avg_daily_spend": number\n'
                '"alerts": [\n'
                '    {"type": "string", "message": "string", "url": "string|null"}\n'
                '],\n'
                '"advice": ["string"]\n'
                "}\n"
                "Reference Lancaster University's services: ASK money advice, LUSU hardship fund, campus store discounts."
            )},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,   
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    
def build_finance_prompt(req: FinanceRequest) -> str:
    """Build structured prompt for AI analysis."""
    expenses_text = "\n".join([
        f"- {e.date}: £{e.amount} | {e.description} | {e.merchant}"
        for e in req.expenses
    ])

    return f"""Lancaster University student {req.student_id} expenses:
{expenses_text}

Income sources: {', '.join(req.income_sources) or 'unknown'}

Analyse for:
1. Risky spending patterns (food > 40%, frequent takeaways)
2. Bursary/hardship fund eligibility signals.
3. Lancaster-specific savings (campus store, shuttles, bulk cooking).
4. Practical next steps.

Return analysis as JSON only."""

def parse_ai_response(ai_json: str, total_spent: Decimal, expenses: List[Expense]) -> FinanceResponse:
    """Core logic: Parse and validate AI JSON response into typed model.
    Unit testable business logic.
    """
    try:
        raw = json.loads(ai_json)

        # Calculate deterministic values
        days_span = (max(e.date for e in expenses) - min(e.date for e in expenses)).days + 1
        avg_daily = float(total_spent / Decimal(days_span)) if days_span > 0 else 0

        # Default categorisation
        categorisation = CategorySummary()

        # Build alerts if AI does not provide them
        alerts = raw.get("alerts", [])
        if total_spent > 500:
            alerts.append({
                "type": "high_spend",
                "message": "Weekly spending exceeds £500. Review ASK money advice.",
                "url": "https://portal.lancaster.ac.uk/ask/money/"
            })
        
        return FinanceResponse(
            summary = {
                "total_spent": float(total_spent),
                "avg_daily_spend": avg_daily,
                **{k: v for k,v in raw.items() if k in ["risk_level", "risk_factors"]}
            },
            categorisation = categorisation,
            alerts = [Alert(**alert) for alert in alerts],
            advice = raw.get("advice", ["Track weekly spending"])
        )
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise ValueError(f"Invalid AI response format: {e}")

@app.post("/feature", response_model=FinanceResponse)
async def analyze_finances(req: FinanceRequest):
    logger.info("Finance analysis for student %s (%d expenses)", req.student_id, len(req.expenses))

    try:
        total_spent = sum(e.amount for e in req.expenses)
        prompt = build_finance_prompt(req)

        ai_response = await call_ai_model(prompt)
        result = parse_ai_response(ai_response, total_spent, req.expenses)

        logger.info("Analysis complete for %s: risk=%s", req.student_id, result.summary.get("risk_level"))
        return result
    except ValueError as ve:
        logger.warning("AI parsing error: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        logger.error("AI service error: %s", re)
        raise HTTPException(status_code=502, detail="Financial analysis service unavailable")
    except Exception as e:
        logger.exception("Unexpected error for student %s", req.student_id)
        raise HTTPException(status_code=500, detail="Internal server error")