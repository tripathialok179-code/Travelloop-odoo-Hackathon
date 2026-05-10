
app.register_blueprint(ai_bp)from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.trip_routes import trip_bp
from routes.ai_routes import ai_bp
from routes.budget_routes import budget_bp
from routes.notes_routes import notes_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(trip_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(notes_bp)

@app.route('/')
def home():
    return {'message': 'TravelLoop API Running'}

if __name__ == '__main__':
    app.run(debug=True)
