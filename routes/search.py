from flask import Blueprint, jsonify

search_bp = Blueprint('search', __name__)

@search_bp.route('/search-city/<query>')
def search_city(query):
    # In a hackathon, you can use a local JSON list for speed
    cities = [
        {"name": "Paris", "country": "France", "cost_index": "High"},
        {"name": "Mumbai", "country": "India", "cost_index": "Medium"}
    ]
    results = [c for c in cities if query.lower() in c['name'].lower()]
    return jsonify(results)