import pytest
from src.web.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"N100 Financial Screener" in response.data

def test_screener_api_endpoint(client):
    response = client.post('/api/v1/screener/run', json={'preset': 'quality_compounder'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'data' in json_data
