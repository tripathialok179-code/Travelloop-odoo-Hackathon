import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from config import Config
from models import db

# Import Blueprints
from routes.auth import auth_bp
from routes.trips import trips_bp
from routes.ai import ai_bp
from routes.search import search_bp
from routes.cities import cities_bp
from routes.share import share_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)

    # Register Blueprints with appropriate prefixes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(cities_bp, url_prefix='/api/cities')
    app.register_blueprint(share_bp, url_prefix='/api/share')

    # Frontend Page Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/create-trip')
    def create_trip():
        return render_template('create_trip.html')

    @app.route('/trip/workspace/<int:trip_id>')
    def workspace(trip_id):
        return render_template('trip_workspace.html', trip_id=trip_id)

    # API for City Images (Unsplash Integration)
    @app.route('/api/city-image/<city_name>')
    def get_city_image(city_name):
        # In production, use os.getenv('UNSPLASH_ACCESS_KEY')
        image_url = f"https://source.unsplash.com/featured/?{city_name},travel"
        return jsonify({"url": image_url})

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create all tables in the MySQL/SQLite database
        db.create_all()
    app.run(debug=True, port=5000)
