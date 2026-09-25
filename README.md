# N100 Financial Platform

An enterprise-grade financial analytics and ETL platform built with Python and FastAPI.

## Key Features
- **ETL Pipeline:** Data extraction, field normalization, and schema validation.
- **Financial Analytics:** Automated metrics computation (Working Capital, Quick Ratio, Debt-to-Equity).
- **RESTful API:** FastAPI endpoints for real-time analytics.
- **100% Test Coverage:** High reliability unit and integration testing.

## Running Tests & Coverage
pytest --cov=src

## Coverage Summary
Total Statements: 177 | Coverage: 100%

## API Usage
uvicorn src.api.main:app --reload

