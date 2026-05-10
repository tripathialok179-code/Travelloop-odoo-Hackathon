from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# --- MOCK DATA FOR FRONTEND TESTING ---
MOCK_TRIPS = [
    {"id": 1, "name": "Paris Getaway", "date": "June 2026", "cities": 1, "cost": 1200, "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"},
    {"id": 2, "name": "Tokyo Adventure", "date": "Oct 2026", "cities": 3, "cost": 3500, "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf"}
]

# --- ROUTES TO CHECK YOUR FRONTEND ---

@app.route('/')
def index():
    """Renders the Hero/Landing Page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Renders the Login Screen"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Renders the Dashboard with Mock Trips"""
    return render_template('dashboard.html', trips=MOCK_TRIPS)

@app.route('/trip/workspace/<int:trip_id>')
def workspace(trip_id):
    """Renders the Itinerary Builder"""
    return render_template('trip_workspace.html', trip_id=trip_id)

# --- MOCK API FOR UNSPLASH IMAGES ---
@app.route('/api/city-image/<city_name>')
def get_city_image(city_name):
    """
    Simulates a backend call to Unsplash.
    In a real app, you'd use your API key here.
    """
    # Placeholder Logic: Returns a high-quality stock photo based on the city name
    image_url = f"https://source.unsplash.com/featured/?{city_name},travel"
    return jsonify({"url": image_url})

if __name__ == '__main__':
    print("Traveloop Prototype Running at http://127.0.0.1:5000")
    app.run(debug=True)