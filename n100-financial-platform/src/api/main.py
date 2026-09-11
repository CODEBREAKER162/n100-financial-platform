from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analytics.ratios import (
    calculate_debt_to_equity,
    calculate_quick_ratio,
)

app = FastAPI()


class DebtToEquityRequest(BaseModel):
    total_debt: float
    total_equity: float


class QuickRatioRequest(BaseModel):
    cash: float
    marketable_securities: float
    receivables: float
    current_liabilities: float


@app.get("/")
def read_root():
    return {"message": "API is running successfully"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analytics/debt-to-equity")
def get_debt_to_equity(data: DebtToEquityRequest):
    try:
        ratio = calculate_debt_to_equity(data.total_debt, data.total_equity)
        return {"ratio": ratio}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analytics/quick-ratio")
def get_quick_ratio(data: QuickRatioRequest):
    try:
        ratio = calculate_quick_ratio(
            data.cash,
            data.marketable_securities,
            data.receivables,
            data.current_liabilities,
        )
        return {"ratio": ratio}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
