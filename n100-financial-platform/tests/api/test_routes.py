import pytest
from unittest.mock import patch
from src.web.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_routes_error_handling(client):
    response = client.get('/api/v1/resource/invalid_id')
    assert response.status_code in (400, 404)

    with patch('src.screener.engine.screen_stocks', side_effect=ValueError('Invalid filter parameter')):
        response = client.post('/api/v1/screen', json={'invalid_param': True})
        assert response.status_code in (400, 500)
        assert b'Invalid filter parameter' in response.data or 'error' in response.get_json()
