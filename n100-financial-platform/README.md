# N100 Financial Intelligence Platform

A production-ready financial screening and intelligence platform built for Nifty 100 stocks. Designed to run completely in pure Python to comply with strict Windows AppLocker / DLL execution policies.

## Features
- Interactive UI: Streamlit dashboard supporting custom metric filtering, qualitative pros/cons analysis, and K-Means peer clustering visualization.
- REST API: FastAPI endpoints providing programmatic access to screening results, stock insights, and cluster groupings.
- Offline Batch Reporting: Automated CLI script to generate structured CSV and PDF reports via ReportLab.
- Pure-Python Analytics: Custom implementations of Z-score normalization and K-Means clustering to eliminate C-extension dependencies.

## Project Structure
- data/ : Stock datasets (nifty100.csv)
- reports/ : Generated CSV/PDF summary outputs
- scripts/generate_reports.py : Batch execution script
- src/api/routes.py : FastAPI REST routes
- src/screener/engine.py : Pure-Python screening & clustering engine
- src/screener/pdf_generator.py : ReportLab PDF generator
- src/web/streamlit_app.py : Streamlit Web UI
- tests/test_screener.py : Verified Pytest suite

## Quick Start Commands

### 1. Launch Streamlit Dashboard
$env:PYTHONPATH="."
streamlit run src/web/streamlit_app.py

### 2. Launch FastAPI Server
$env:PYTHONPATH="."
uvicorn src.api.routes:app --reload --port 8000

### 3. Run Batch Reports
$env:PYTHONPATH="."
python scripts/generate_reports.py

### 4. Run Unit Tests
$env:PYTHONPATH="."
pytest tests/test_screener.py

