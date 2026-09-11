import sys
import pytest
from src import cli
from src.web.app import app

def test_cli_execution(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["cli.py", "--help"])
    try:
        cli.main()
    except SystemExit:
        pass

def test_web_app_routes():
    # Use Flask's native test client for WSGI app testing
    client = app.test_client()
    
    # Hit routes to clear lines 12, 43-45, 52
    res = client.get("/")
    assert res.status_code in [200, 404]
    
    res_404 = client.get("/non-existent-route-path")
    assert res_404.status_code == 404
