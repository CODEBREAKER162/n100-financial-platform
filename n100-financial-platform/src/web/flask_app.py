from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "N100 Financial Screener", 200

@app.route("/api/v1/screener/run", methods=["POST"])
def run_screener():
    return {"status": "success", "data": []}, 200

@app.route("/api/v1/screen", methods=["POST"])
def screen_endpoint():
    from src.screener.engine import screen_stocks
    data = request.get_json() or {}
    try:
        results = screen_stocks(data)
        return {"status": "success", "data": results}, 200
    except ValueError as e:
        return {"error": str(e)}, 400
