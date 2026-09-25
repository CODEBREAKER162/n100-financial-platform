import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.screener.engine import screen_stocks, generate_insights, cluster_stocks
from src.api.routes import app
from scripts.generate_reports import run_batch_export

client = TestClient(app)

def test_screen_stocks_default():
    results = screen_stocks()
    assert isinstance(results, list)
    assert len(results) > 0

def test_screen_stocks_filter():
    results = screen_stocks({"max_pe": 20})
    for stock in results:
        assert stock["pe_ratio"] <= 20

def test_generate_insights():
    stock = {"symbol": "TCS", "pe_ratio": 29.1, "roe": 48.5}
    insights = generate_insights(stock)
    assert "pros" in insights
    assert "cons" in insights
    assert len(insights["pros"]) > 0

def test_cluster_stocks():
    df = cluster_stocks(n_clusters=3)
    assert "cluster" in df.columns
    assert "cluster_label" in df.columns
    assert len(df["cluster"].unique()) <= 3

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to N100 Financial Intelligence API"

def test_api_screener_endpoint():
    response = client.get("/api/screener?max_pe=25")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "data" in data

def test_batch_report_execution(tmp_path):
    run_batch_export()
    assert (Path("reports") / "nifty100_summary.csv").exists()
    assert (Path("reports") / "nifty100_summary.pdf").exists()
