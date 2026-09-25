import pandas as pd
import os
import math
import random

def load_data():
    possible_paths = ["data/nifty100.csv", "data/stocks.csv", "src/data/nifty100.csv"]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
            
    return pd.DataFrame([
        {"symbol": "RELIANCE", "company": "Reliance Industries", "pe_ratio": 24.5, "roe": 14.2, "sector": "Energy"},
        {"symbol": "TCS", "company": "Tata Consultancy Services", "pe_ratio": 29.1, "roe": 48.5, "sector": "IT"},
        {"symbol": "HDFCBANK", "company": "HDFC Bank", "pe_ratio": 19.8, "roe": 16.8, "sector": "Banking"},
        {"symbol": "INFY", "company": "Infosys", "pe_ratio": 25.3, "roe": 31.4, "sector": "IT"},
        {"symbol": "ICICIBANK", "company": "ICICI Bank", "pe_ratio": 17.2, "roe": 18.5, "sector": "Banking"},
        {"symbol": "BHARTIARTL", "company": "Bharti Airtel", "pe_ratio": 42.1, "roe": 12.6, "sector": "Telecom"},
        {"symbol": "ITC", "company": "ITC Limited", "pe_ratio": 26.8, "roe": 29.1, "sector": "FMCG"},
        {"symbol": "LT", "company": "Larsen & Toubro", "pe_ratio": 31.2, "roe": 15.4, "sector": "Construction"},
        {"symbol": "HINDUNILVR", "company": "Hindustan Unilever", "pe_ratio": 55.4, "roe": 20.2, "sector": "FMCG"},
        {"symbol": "TATAMOTORS", "company": "Tata Motors", "pe_ratio": 10.5, "roe": 45.2, "sector": "Automobile"}
    ])

def generate_insights(stock):
    pros = []
    cons = []
    
    if stock.get("roe", 0) > 20:
        pros.append("High capital efficiency with ROE > 20%")
    elif stock.get("roe", 0) < 15:
        cons.append("Subdued Return on Equity underperforming peer averages")
        
    if stock.get("pe_ratio", 0) < 20:
        pros.append("Attractive valuation trading below 20x P/E ratio")
    elif stock.get("pe_ratio", 0) > 40:
        cons.append("Premium valuation multiple exceeding industry norms")

    return {
        "pros": pros if pros else ["Stable operational performance"],
        "cons": cons if cons else ["No major valuation warnings"]
    }

def cluster_stocks(n_clusters=3):
    df = load_data().copy()
    if df.empty:
        return df

    features = df[["pe_ratio", "roe"]].values.tolist()
    
    # Standardize Features (Z-Score)
    pe_vals = [f[0] for f in features]
    roe_vals = [f[1] for f in features]
    
    pe_mean = sum(pe_vals) / len(pe_vals)
    pe_std = (sum((x - pe_mean) ** 2 for x in pe_vals) / len(pe_vals)) ** 0.5 or 1.0
    
    roe_mean = sum(roe_vals) / len(roe_vals)
    roe_std = (sum((x - roe_mean) ** 2 for x in roe_vals) / len(roe_vals)) ** 0.5 or 1.0

    scaled = [[(f[0] - pe_mean) / pe_std, (f[1] - roe_mean) / roe_std] for f in features]

    # Pure Python K-Means
    random.seed(42)
    centroids = random.sample(scaled, min(n_clusters, len(scaled)))
    
    assignments = [0] * len(scaled)
    for _ in range(20):  # Convergence iterations
        # Assign points to nearest centroid
        for i, point in enumerate(scaled):
            distances = [math.hypot(point[0] - c[0], point[1] - c[1]) for c in centroids]
            assignments[i] = distances.index(min(distances))
        
        # Update centroids
        new_centroids = []
        for k in range(len(centroids)):
            cluster_points = [scaled[i] for i, a in enumerate(assignments) if a == k]
            if cluster_points:
                avg_x = sum(p[0] for p in cluster_points) / len(cluster_points)
                avg_y = sum(p[1] for p in cluster_points) / len(cluster_points)
                new_centroids.append([avg_x, avg_y])
            else:
                new_centroids.append(centroids[k])
        centroids = new_centroids

    df["cluster"] = assignments
    cluster_names = {
        0: "Cluster A (High Quality / Growth)",
        1: "Cluster B (Value / Moderate ROE)",
        2: "Cluster C (Premium Multiple / High Risk)",
        3: "Cluster D (Emerging)",
        4: "Cluster E (Niche)"
    }
    df["cluster_label"] = df["cluster"].map(lambda x: cluster_names.get(x, f"Cluster {x}"))
    return df

def screen_stocks(filter_data=None):
    df = load_data()
    if df is None or df.empty:
        return []
        
    if not filter_data:
        return df.to_dict(orient="records")

    if "max_pe" in filter_data and "pe_ratio" in df.columns:
        df = df[df["pe_ratio"] <= filter_data["max_pe"]]

    if "min_roe" in filter_data and "roe" in df.columns:
        df = df[df["roe"] >= filter_data["min_roe"]]

    preset = filter_data.get("preset")
    if preset == "value_play" and "pe_ratio" in df.columns:
        df = df[df["pe_ratio"] < 25]
    elif preset == "quality_compounder" and "roe" in df.columns:
        df = df[df["roe"] > 15]

    return df.to_dict(orient="records")
    
