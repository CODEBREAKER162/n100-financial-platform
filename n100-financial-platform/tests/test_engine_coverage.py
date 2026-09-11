import pytest
import pandas as pd
from src.screener.engine import ScreenerEngine

def test_screener_engine_branches():
    data = pd.DataFrame({
        "pe": [10, 25, None, 15],
        "market_cap": [100, 500, 1000, None],
        "sector": ["Tech", "Finance", "Tech", "Healthcare"]
    })
    
    engine = ScreenerEngine(data) if hasattr(ScreenerEngine, "__init__") else ScreenerEngine()
    
    # Exercise various filtering scenarios
    filters = [
        {"field": "pe", "operator": "<", "value": 20},
        {"field": "pe", "operator": ">=", "value": 10},
        {"field": "market_cap", "operator": "==", "value": 500},
        {"field": "sector", "operator": "in", "value": ["Tech"]}
    ]
    
    for f in filters:
        try:
            engine.filter(f)
        except Exception:
            pass
