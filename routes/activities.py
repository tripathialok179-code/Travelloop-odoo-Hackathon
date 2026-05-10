from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.activity import Activity

activities_bp = Blueprint('activities', __name__, url_prefix='/api/activities')


# GET all activities
@activities_bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([a.to_dict() for a in activities]), 200


# GET single activity
@activities_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return jsonify(activity.to_dict()), 200


# CREATE activity
@activities_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json()

    new_activity = Activity(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        location=data.get('location'),
        city=data.get('city'),
        country=data.get('country'),
        price=data.get('price', 0.0),
        rating=data.get('rating', 0.0),
        review_count=data.get('review_count', 0),
        image_url=data.get('image_url')
    )

    db.session.add(new_activity)
    db.session.commit()

    return jsonify(new_activity.to_dict()), 201


# UPDATE activity
@activities_bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    data = request.get_json()

    activity.title = data.get('title', activity.title)
    activity.description = data.get('description', activity.description)
    activity.category = data.get('category', activity.category)
    activity.location = data.get('location', activity.location)
    activity.city = data.get('city', activity.city)
    activity.country = data.get('country', activity.country)
    activity.price = data.get('price', activity.price)
    activity.rating = data.get('rating', activity.rating)
    activity.review_count = data.get('review_count', activity.review_count)
    activity.image_url = data.get('image_url', activity.image_url)

    db.session.commit()

    return jsonify(activity.to_dict()), 200


# DELETE activity
@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    db.session.delete(activity)
    db.session.commit()

    return jsonify({"message": "Activity deleted successfully"}), 200