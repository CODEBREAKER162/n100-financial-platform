from flask import Flask, jsonify
from src.api.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api/v1')

@app.route('/')
def home():
    return "<h1>N100 Financial Screener</h1>", 200
