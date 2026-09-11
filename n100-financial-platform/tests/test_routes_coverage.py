import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_api_routes_all():
    response = client.get("/")
    assert response.status_code in [200, 404]

    for route in app.routes:
        if hasattr(route, "path"):
            # Try GET request
            res_get = client.get(route.path)
            assert res_get.status_code in [200, 400, 404, 405, 422]
            
            # Try POST request for POST endpoints
            res_post = client.post(route.path, json={})
            assert res_post.status_code in [200, 400, 404, 405, 422]
