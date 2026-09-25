from fastapi import FastAPI, Query
from typing import Optional
from src.screener.engine import screen_stocks, generate_insights, cluster_stocks

app = FastAPI(
    title="N100 Financial Intelligence API",
    description="REST Endpoints for Nifty 100 stock screening, financial metrics, and peer clustering.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to N100 Financial Intelligence API"}

@app.get("/api/screener")
def get_screener_results(
    max_pe: Optional[float] = Query(None, description="Maximum P/E Ratio filter"),
    min_roe: Optional[float] = Query(None, description="Minimum ROE (%) filter"),
    preset: Optional[str] = Query(None, description="Preset strategy: quality_compounder or value_play")
):
    filter_data = {}
    if max_pe is not None:
        filter_data["max_pe"] = max_pe
    if min_roe is not None:
        filter_data["min_roe"] = min_roe
    if preset:
        filter_data["preset"] = preset
        
    results = screen_stocks(filter_data)
    return {"count": len(results), "data": results}

@app.get("/api/insights/{symbol}")
def get_stock_insights(symbol: str):
    all_stocks = screen_stocks()
    stock = next((s for s in all_stocks if s["symbol"].upper() == symbol.upper()), None)
    if not stock:
        return {"error": f"Stock symbol '{symbol}' not found"}
    
    insights = generate_insights(stock)
    return {"symbol": symbol.upper(), "stock_data": stock, "insights": insights}

@app.get("/api/clusters")
def get_stock_clusters(n_clusters: int = 3):
    df_clustered = cluster_stocks(n_clusters=n_clusters)
    return {"count": len(df_clustered), "clusters": df_clustered.to_dict(orient="records")}
