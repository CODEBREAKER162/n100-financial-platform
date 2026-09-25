import os
import pytest
import pandas as pd

OUTPUT_DIR = "output"

def test_cashflow_intelligence_export_exists():
    excel_path = os.path.join(OUTPUT_DIR, "cashflow_intelligence.xlsx")
    assert os.path.exists(excel_path), "Cashflow intelligence excel file is missing"
    df = pd.read_excel(excel_path)
    assert len(df) == 92, f"Expected 92 rows, got {len(df)}"

def test_distress_alerts_export_exists():
    csv_path = os.path.join(OUTPUT_DIR, "distress_alerts.csv")
    assert os.path.exists(csv_path), "Distress alerts CSV is missing"
    df = pd.read_csv(csv_path)
    assert len(df) == 7, f"Expected 7 flagged companies, got {len(df)}"

def test_pdf_tearsheets_generated():
    pdf_dir = os.path.join(OUTPUT_DIR, "pdf_tearsheets")
    assert os.path.exists(pdf_dir), "PDF tearsheets directory is missing"
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    assert len(pdfs) == 92, f"Expected 92 PDFs, got {len(pdfs)}"

