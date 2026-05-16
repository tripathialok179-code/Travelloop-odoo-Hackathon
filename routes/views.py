from flask import Blueprint, render_template, g, redirect, url_for, request
from models import db
from models.trip import Trip

views_bp = Blueprint('views', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@views_bp.route('/')
@views_bp.route('/login')
def login():
    if g.user:
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@views_bp.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=g.user.id).all()
    return render_template('dashboard.html', trips=trips)

@views_bp.route('/create-trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    if request.method == 'POST':
        title = request.form.get('title')
        destination = request.form.get('destination')
        start_point = request.form.get('start_point')
        transport_mode = request.form.get('transport_mode')
        vehicle_model = request.form.get('vehicle_model')
        num_people = request.form.get('num_people', 1)
        days = request.form.get('days', 7)
        
        new_trip = Trip(
            user_id=g.user.id,
            title=title,
            destination=destination,
            start_point=start_point,
            transport_mode=transport_mode,
            vehicle_model=vehicle_model,
            num_people=int(num_people) if num_people else 1,
            days=int(days) if days else 7
        )
        db.session.add(new_trip)
        db.session.commit()
        return redirect(url_for('views.itinerary_view', trip_id=new_trip.id))
        
    return render_template('create_trip.html')

@views_bp.route('/my-trips')
@login_required
def my_trips():
    trips = Trip.query.filter_by(user_id=g.user.id).all()
    return render_template('my_trips.html', trips=trips)

@views_bp.route('/trip/<int:trip_id>/builder')
@login_required
def itinerary_builder(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    import json
    ai_logistics = None
    if trip.ai_logistics:
        try:
            ai_logistics = json.loads(trip.ai_logistics)
        except:
            pass
    return render_template('itinerary_builder.html', trip=trip, ai_logistics=ai_logistics)

@views_bp.route('/itinerary/<int:trip_id>')
@login_required
def itinerary_view(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    import json
    ai_summary = None
    if trip.ai_summary:
        try:
            ai_summary = json.loads(trip.ai_summary)
        except:
            pass
    return render_template('itinerary_view.html', trip=trip, ai_summary=ai_summary)

@views_bp.route('/delete-trip/<int:trip_id>', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=g.user.id).first_or_404()
    db.session.delete(trip)
    db.session.commit()
    return redirect(url_for('views.dashboard'))

@views_bp.route('/city-search')
@login_required
def city_search():
    return render_template('city_search.html')

@views_bp.route('/trip/<int:trip_id>/budget')
@login_required
def budget(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    import json
    ai_budget_data = None
    if trip.ai_budget:
        try:
            parsed = json.loads(trip.ai_budget)
            if isinstance(parsed, dict) and "type" in parsed:
                ai_budget_data = parsed
            else:
                ai_budget_data = {"type": "selected", "data": parsed}
        except:
            pass
    return render_template('budget.html', trip=trip, ai_budget_data=ai_budget_data)

@views_bp.route('/trip/<int:trip_id>/packing')
@login_required
def packing(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    import json
    ai_packing = None
    if trip.ai_packing:
        try:
            ai_packing = json.loads(trip.ai_packing)
        except:
            pass
    return render_template('packing.html', trip=trip, ai_packing=ai_packing)

@views_bp.route('/shared/<int:trip_id>')
def shared_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('shared_trip.html', trip=trip)

@views_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@views_bp.route('/trip/<int:trip_id>/notes')
@login_required
def trip_notes(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trip_notes.html', trip=trip)
