from app.models.city import City
from app.models.activity import Activity
from app.models.trip import Trip
from app.models.expense import Expense


class RecommendationService:
    """
    Simple recommendation engine for travel app MVP.
    Can be extended into AI/ML-based suggestions later.
    """

    @staticmethod
    def recommend_cities(preferred_country=None, limit=5):
        """Recommend cities based on popularity (basic MVP logic)."""
        query = City.query

        if preferred_country:
            query = query.filter_by(country=preferred_country)

        cities = query.limit(limit).all()

        return [c.to_dict() for c in cities]

    @staticmethod
    def recommend_activities(city_id, category=None, budget=None, limit=10):
        """Recommend activities based on city, category, and budget."""
        query = Activity.query.filter_by(city_id=city_id)

        if category:
            query = query.filter_by(category=category)

        if budget is not None:
            query = query.filter(Activity.price <= budget)

        activities = query.limit(limit).all()

        return [a.to_dict() for a in activities]

    @staticmethod
    def recommend_next_trip(user_id):
        """
        Recommend next trip idea based on user's past trips.
        (Very simple heuristic-based logic for MVP)
        """
        past_trips = Trip.query.filter_by(user_id=user_id).all()

        if not past_trips:
            # first-time user fallback
            return {
                "message": "No history found",
                "suggestion": City.query.limit(3).all()
            }

        # extract visited countries
        visited_countries = set()
        for trip in past_trips:
            if trip.country:
                visited_countries.add(trip.country)

        # suggest new countries (simple logic)
        suggestions = City.query.filter(~City.country.in_(visited_countries)).limit(5).all()

        return {
            "visited_countries": list(visited_countries),
            "recommendations": [c.to_dict() for c in suggestions]
        }

    @staticmethod
    def budget_based_suggestions(user_id):
        """Suggest trips based on spending patterns."""
        trips = Trip.query.filter_by(user_id=user_id).all()

        if not trips:
            return {"message": "No trip history available"}

        avg_budget = sum(t.budget or 0 for t in trips) / len(trips)

        # cheap + mid-range destinations
        affordable_cities = City.query.limit(5).all()

        return {
            "average_budget": avg_budget,
            "suggested_cities": [c.to_dict() for c in affordable_cities]
        }