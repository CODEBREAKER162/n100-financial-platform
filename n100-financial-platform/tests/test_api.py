from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running successfully"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_debt_to_equity_success():
    response = client.post(
        "/analytics/debt-to-equity",
        json={"total_debt": 100.0, "total_equity": 50.0},
    )
    assert response.status_code == 200
    assert response.json() == {"ratio": 2.0}


def test_get_debt_to_equity_zero_equity():
    response = client.post(
        "/analytics/debt-to-equity",
        json={"total_debt": 100.0, "total_equity": 0.0},
    )
    assert response.status_code == 400


def test_get_quick_ratio_success():
    payload = {
        "cash": 1000.0,
        "marketable_securities": 500.0,
        "receivables": 200.0,
        "current_liabilities": 400.0,
    }
    response = client.post("/analytics/quick-ratio", json=payload)
    assert response.status_code == 200
    assert response.json() == {"ratio": 4.25}


def test_get_quick_ratio_zero_liabilities():
    payload = {
        "cash": 1000.0,
        "marketable_securities": 500.0,
        "receivables": 200.0,
        "current_liabilities": 0.0,
    }
    response = client.post("/analytics/quick-ratio", json=payload)
    assert response.status_code == 400
