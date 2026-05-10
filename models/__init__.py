from flask_sqlalchemy import SQLAlchemy

# Initialize the shared database object
db = SQLAlchemy()

# Import all models here so they are registered with the DB
from models.user import User
from models.trip import Trip
from models.activity import Activity
from models.city import City
from models.expense import Expense
from models.packing import PackingItem

__all__ = ["db", "User", "Trip", "Activity", "City", "Expense", "PackingItem"]
