import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(title="N100 Financial Analytics API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

@app.get("/")
def read_root():
    return {"status": "online", "message": "N100 Financial Platform API"}

@app.get("/api/cashflow-intelligence")
def get_cashflow_intelligence():
    file_path = os.path.join(OUTPUT_DIR, "cashflow_intelligence.xlsx")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Cash flow intelligence file not found")
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")

@app.get("/api/distress-alerts")
def get_distress_alerts():
    file_path = os.path.join(OUTPUT_DIR, "distress_alerts.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Distress alerts file not found")
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

@app.get("/api/tearsheet/{company_id}")
def download_tearsheet(company_id: str):
    pdf_path = os.path.join(OUTPUT_DIR, "pdf_tearsheets", f"{company_id}_tearsheet.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail=f"Tearsheet PDF for {company_id} not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{company_id}_tearsheet.pdf")

