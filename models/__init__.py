from flask_sqlalchemy import SQLAlchemy

# Initialize the shared database object
db = SQLAlchemy()

# Import all models here so they are registered with the DB
from models.user import User
from models.trip import Trip

__all__ = ["db", "User", "Trip"]
