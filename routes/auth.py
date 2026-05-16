from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            new_user = User(name=name, email=email, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Incorrect email or password.', category='error')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('views.login'))
