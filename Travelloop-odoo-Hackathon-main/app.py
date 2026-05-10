import os

from flask import Flask
from flask import render_template

from dotenv import load_dotenv

from config import Config

from models.trip import db

from routes.auth import auth_bp
from routes.ai import ai_bp


# LOAD ENV VARIABLES
load_dotenv()


def create_app():

    app = Flask(__name__)

    # LOAD CONFIG
    app.config.from_object(Config)

    # OPTIONAL API KEY
    app.config['UNSPLASH_KEY'] = os.getenv(
        'UNSPLASH_ACCESS_KEY'
    )

    # INIT DATABASE
    db.init_app(app)

    # REGISTER BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)

    # -----------------------------
    # HOME PAGE
    # -----------------------------
    @app.route('/')
    def home():

        return render_template(
            'trip_workspace.html'
        )

    # -----------------------------
    # DASHBOARD PAGE
    # -----------------------------
    @app.route('/dashboard')
    def dashboard():

        return render_template(
            'dashboard.html'
        )

    return app


# -----------------------------
# MAIN ENTRY
# -----------------------------
if __name__ == '__main__':

    app = create_app()

    with app.app_context():

        # CREATE SQLITE TABLES
        db.create_all()

    app.run(debug=True)