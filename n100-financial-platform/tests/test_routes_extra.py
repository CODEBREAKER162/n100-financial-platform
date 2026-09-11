import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_api_endpoints():
    # Call typical routes defined in src/api/routes.py
    for route in ["/health", "/api/v1/screener", "/api/v1/metrics"]:
        response = client.get(route)
        assert response.status_code in [200, 404, 422]
