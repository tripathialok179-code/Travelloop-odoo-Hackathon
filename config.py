import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///traveloop.db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        'hackathon-super-secret-key'
    )