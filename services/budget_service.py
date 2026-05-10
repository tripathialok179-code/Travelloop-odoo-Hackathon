from app.extensions import db
from app.models.trip import Trip
from app.models.expense import Expense


class BudgetService:
    """
    Service layer for all budget & expense business logic.
    Keeps routes clean and logic centralized.
    """

    @staticmethod
    def calculate_trip_summary(trip_id):
        trip = Trip.query.get_or_404(trip_id)
        expenses = Expense.query.filter_by(trip_id=trip_id).all()

        total_spent = sum(e.amount for e in expenses)
        budget = trip.budget or 0
        remaining = budget - total_spent

        return {
            "trip_id": trip_id,
            "budget": budget,
            "total_spent": total_spent,
            "remaining": remaining,
            "expense_count": len(expenses),
            "status": trip.status
        }

    @staticmethod
    def add_expense(trip_id, user_id, title, amount, category, description=None, currency="INR"):
        trip = Trip.query.get_or_404(trip_id)

        expense = Expense(
            trip_id=trip_id,
            user_id=user_id,
            title=title,
            amount=amount,
            category=category,
            description=description,
            currency=currency
        )

        db.session.add(expense)

        # update trip spending
        trip.total_spent = (trip.total_spent or 0) + amount

        db.session.commit()

        return expense

    @staticmethod
    def update_budget(trip_id, new_budget):
        trip = Trip.query.get_or_404(trip_id)

        trip.budget = new_budget
        db.session.commit()

        return {
            "trip_id": trip_id,
            "new_budget": trip.budget
        }

    @staticmethod
    def get_remaining_budget(trip_id):
        trip = Trip.query.get_or_404(trip_id)

        expenses = Expense.query.filter_by(trip_id=trip_id).all()
        spent = sum(e.amount for e in expenses)

        return {
            "trip_id": trip_id,
            "budget": trip.budget,
            "spent": spent,
            "remaining": (trip.budget or 0) - spent
        }