from flask import Flask, g, session
from config import Config
from models import db
from models.user import User
from routes.views import views_bp
from routes.api import api_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

with app.app_context():
    db.create_all()

app.register_blueprint(views_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
