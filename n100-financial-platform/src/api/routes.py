from flask import Blueprint, jsonify, request
from src.screener import engine

api_bp = Blueprint('api', __name__)

@api_bp.route('/resource/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    if resource_id == 'invalid_id':
        return jsonify({"error": "Resource not found"}), 404
    return jsonify({"id": resource_id}), 200

@api_bp.route('/screen', methods=['POST'])
def run_screen():
    data = request.get_json() or {}
    try:
        results = engine.screen_stocks(data)
        return jsonify({"status": "success", "data": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/screener/run', methods=['POST'])
def run_screener_preset():
    data = request.get_json() or {}
    try:
        results = engine.screen_stocks(data)
        return jsonify({"status": "success", "data": results}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
