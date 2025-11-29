import pytest
from decimal import Decimal
from datetime import date
from app.main import parse_ai_response, FinanceRequest, Expense

def test_parse_ai_response_valid():
    """Unit test core AI parsing logic."""
    ai_json = '''
    {
        "risk_level": "medium",
        "risk_factors": ["high food spend"],
        "total_spent": 250.00,
        "avg_daily_spend": 12.5,
        "alerts": [{"type": "food_risk", "message": "Check ASK budgeting advice", "url": "https://portal.lancaster.ac.uk/ask/money/managing/"}],
        "advice": ["Learn to cook simple meals in bulk."]
    }
    '''

    expenses = [Expense(date=date(2025,11,25), amount=Decimal('75.00'), description="test", merchant="test")]

    total_spent = sum(e.amount for e in expenses)

    result = parse_ai_response(ai_json, total_spent=total_spent, expenses=expenses)

    assert result.summary["risk_level"] == "medium"
    assert len(result.alerts) >= 1
    assert "cook" in result.advice[0]

def test_parse_ai_response_invalid_json():
    """Test error handling for invalid JSON."""
    with pytest.raises(ValueError):
        parse_ai_response("invalid json", Decimal('100'), [])