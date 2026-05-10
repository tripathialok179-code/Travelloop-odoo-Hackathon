from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.city import City
from app.models.activity import Activity
from app.models.trip import Trip

search_bp = Blueprint('search', __name__, url_prefix='/api/search')


# GLOBAL SEARCH (cities + activities + trips)
@search_bp.route('/', methods=['GET'])
def global_search():
    query = request.args.get('q', '').strip()
    category = request.args.get('type', '').strip()  # city | activity | trip | all

    if not query:
        return jsonify({"message": "Search query 'q' is required"}), 400

    results = {
        "cities": [],
        "activities": [],
        "trips": []
    }

    # search cities
    if category in ['', 'all', 'city', 'cities']:
        cities = City.query.filter(City.name.ilike(f"%{query}%")).all()
        results["cities"] = [c.to_dict() for c in cities]

    # search activities
    if category in ['', 'all', 'activity', 'activities']:
        activities = Activity.query.filter(Activity.title.ilike(f"%{query}%")).all()
        results["activities"] = [a.to_dict() for a in activities]

    # search trips
    if category in ['', 'all', 'trip', 'trips']:
        trips = Trip.query.filter(Trip.title.ilike(f"%{query}%")).all()
        results["trips"] = [t.to_dict() for t in trips]

    return jsonify({
        "query": query,
        "results": results
    }), 200