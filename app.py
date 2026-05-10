from flask import Flask, render_template
from config import Config
from models.trip import db
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)

    @app.route('/')
    def dashboard():
        # Central hub showing upcoming trips (cite: 32, 33)
        return render_template('dashboard.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() # Generates MySQL tables based on models
    app.run(debug=True)