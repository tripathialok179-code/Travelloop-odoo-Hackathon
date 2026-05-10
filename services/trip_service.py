from app.extensions import db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.packing import PackingItem
from app.models.activity import Activity


class TripService:
    """
    Service layer for trip-related business logic.
    Handles orchestration between trips, expenses, packing, and activities.
    """

    @staticmethod
    def create_trip(data):
        """Create a new trip with validated data."""
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

        return trip

    @staticmethod
    def get_trip_dashboard(trip_id):
        """Return full trip overview (core hackathon feature)."""
        trip = Trip.query.get_or_404(trip_id)

        expenses = Expense.query.filter_by(trip_id=trip_id).all()
        packing_items = PackingItem.query.filter_by(trip_id=trip_id).all()

        activities = []
        if trip.city_id:
            activities = Activity.query.filter_by(city_id=trip.city_id).all()

        total_spent = sum(e.amount for e in expenses)
        remaining_budget = (trip.budget or 0) - total_spent

        return {
            "trip": trip.to_dict(),
            "expenses": [e.to_dict() for e in expenses],
            "packing_items": [p.to_dict() for p in packing_items],
            "activities": [a.to_dict() for a in activities],
            "summary": {
                "budget": trip.budget,
                "total_spent": total_spent,
                "remaining_budget": remaining_budget,
                "expense_count": len(expenses)
            }
        }

    @staticmethod
    def update_trip(trip_id, data):
        """Update trip details safely."""
        trip = Trip.query.get_or_404(trip_id)

        for field in [
            "title", "description", "destination", "country",
            "start_date", "end_date", "budget",
            "total_spent", "status", "travelers_count"
        ]:
            if field in data:
                setattr(trip, field, data[field])

        db.session.commit()

        return trip

    @staticmethod
    def delete_trip(trip_id):
        """Delete trip and all related data (basic cleanup)."""
        trip = Trip.query.get_or_404(trip_id)

        Expense.query.filter_by(trip_id=trip_id).delete()
        PackingItem.query.filter_by(trip_id=trip_id).delete()

        db.session.delete(trip)
        db.session.commit()

        return {"message": "Trip deleted successfully"}

    @staticmethod
    def get_user_trips(user_id):
        """Fetch all trips for a user."""
        trips = Trip.query.filter_by(user_id=user_id).all()
        return [t.to_dict() for t in trips]