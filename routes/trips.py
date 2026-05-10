from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Trip, Expense, PackingItem, Activity

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/', methods=['POST'])
def create_trip():
    data = request.get_json()
    
    # Validate required fields as per project mission [cite: 8, 40]
    if not data.get('title') or not data.get('destination'):
        return jsonify({"message": "Title and destination are required"}), 400

    new_trip = Trip(
        title=data['title'],
        description=data.get('description'),
        destination=data['destination'],
        user_id=data.get('user_id', 1), # Default for prototype
        budget=data.get('budget', 0.0),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d') if data.get('start_date') else None,
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d') if data.get('end_date') else None
    )

    db.session.add(new_trip)
    db.session.commit()
    return jsonify(new_trip.to_dict()), 201

@trips_bp.route('/<int:trip_id>/dashboard', methods=['GET'])
def trip_dashboard(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    # Orchestrate summary data for the workspace [cite: 14, 69]
    return jsonify({
        "trip": trip.to_dict(),
        "expenses": [e.to_dict() for e in Expense.query.filter_by(trip_id=trip_id).all()],
        "summary": {
            "spent": sum(e.amount for e in Expense.query.filter_by(trip_id=trip_id).all()),
            "budget": trip.budget
        }
    }), 200
