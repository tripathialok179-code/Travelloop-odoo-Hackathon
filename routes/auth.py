from flask import Blueprint, render_template, redirect, url_for, request
from models.trip import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic to verify email & password (cite: 31)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    # Logic to create new user account (cite: 28)
    return render_template('signup.html')