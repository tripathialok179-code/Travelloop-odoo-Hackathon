from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.packing import PackingItem
from app.models.activity import Activity

trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')


# GET all trips (optionally filter by user)
@trips_bp.route('/', methods=['GET'])
def get_trips():
    user_id = request.args.get('user_id')

    if user_id:
        trips = Trip.query.filter_by(user_id=user_id).all()
    else:
        trips = Trip.query.all()

    return jsonify([t.to_dict() for t in trips]), 200


# GET single trip
@trips_bp.route('/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return jsonify(trip.to_dict()), 200


# CREATE trip
@trips_bp.route('/', methods=['POST'])
def create_trip():
    data = request.get_json()

    if not data.get('title') or not data.get('destination') or not data.get('user_id'):
        return jsonify({"message": "title, destination, user_id are required"}), 400

    trip = Trip(
        title=data.get('title'),
        description=data.get('description'),
        user_id=data.get('user_id'),
        city_id=data.get('city_id'),
        destination=data.get('destination'),
        country=data.get('country'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        budget=data.get('budget', 0.0),
        travelers_count=data.get('travelers_count', 1)
    )

    db.session.add(trip)
    db.session.commit()

    return jsonify(trip.to_dict()), 201


# UPDATE trip
@trips_bp.route('/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    data = request.get_json()

    trip.title = data.get('title', trip.title)
    trip.description = data.get('description', trip.description)
    trip.destination = data.get('destination', trip.destination)
    trip.country = data.get('country', trip.country)
    trip.start_date = data.get('start_date', trip.start_date)
    trip.end_date = data.get('end_date', trip.end_date)
    trip.budget = data.get('budget', trip.budget)
    trip.total_spent = data.get('total_spent', trip.total_spent)
    trip.status = data.get('status', trip.status)
    trip.travelers_count = data.get('travelers_count', trip.travelers_count)

    db.session.commit()

    return jsonify(trip.to_dict()), 200


# DELETE trip
@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    db.session.delete(trip)
    db.session.commit()

    return jsonify({"message": "Trip deleted successfully"}), 200


# TRIP DASHBOARD (FULL OVERVIEW)
@trips_bp.route('/<int:trip_id>/dashboard', methods=['GET'])
def trip_dashboard(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # expenses
    expenses = Expense.query.filter_by(trip_id=trip_id).all()

    # packing items
    packing_items = PackingItem.query.filter_by(trip_id=trip_id).all()

    # activities (linked via city)
    activities = []
    if trip.city_id:
        activities = Activity.query.filter_by(city_id=trip.city_id).all()

    return jsonify({
        "trip": trip.to_dict(),
        "expenses": [e.to_dict() for e in expenses],
        "packing_items": [p.to_dict() for p in packing_items],
        "activities": [a.to_dict() for a in activities]
    }), 200