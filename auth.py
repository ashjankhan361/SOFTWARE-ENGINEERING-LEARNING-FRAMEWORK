
# Import required libraries.
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .app import db
from .models import User
import json

# Initialize the Authentication Blueprint.
# This blueprint defines the routes that can only be accessed only by the
# authenticated users.
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Handles the /login endpoint with GET request method.
    """

    # Redirects to the homepage as Homepage("/") contains Login form.
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Handles the authentication of the user and responsible for provided access
    to the authorized endpoints.
    """

    # Get the email field value.
    email = request.form.get('email')

    # Get the password field value.
    password = request.form.get('password')

    # Check whether the "remember me" was selected.
    remember = True if request.form.get('remember') else False

    # Search for the user by email in the database.
    user = User.query.filter_by(email=email).first()

    # Execute the following if statement only if the user doesn't exists or
    # invalid credentials.
    if not user or not check_password_hash(user.password, password):
        # Send the authentication error message.
        flash('Incorrect Email/Password combination.')

        # Redirect the user to the login page.
        return redirect(url_for('main.index'))

    # If all good then, login the user.
    login_user(user, remember=remember)

    # Redirect to the dashboard.
    return redirect(url_for('auth.dashboard'))

@auth.route('/signup')
def signup():
    """
    Handles the "/signup" endpoint.
    """

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    """
    Handles the logout functionality.
    """

    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/game')
def game():
    """
    Handles the "/game" endpoint.

    For now, this endpoint only displays the selected options and this can
    further be implemented to add actions to start the game.
    """

    options = {
        'education_level': {
            '1': 'Secondary',
            '2': 'Undergraduate',
            '3': 'Graduate',
        },
        'game_experience': {
            '1': 'Experiential Learning',
            '2': '2D',
            '3': 'Quiz',
        },
        'game_mode': {
            '1': 'Single Player',
            '2': 'Multi-player',
        }
    }

    return render_template('game.html', options=options)

@auth.route('/analytics')
def analytics():
    """
    Handles the "/analytics" endpoint and renders the user analytical data.
    """

    # Education level index to name mapping.
    options = {
        'education_level': {
            '1': 'Freshman',
            '2': 'Sophomore',
            '3': 'Junior',
            '4': 'Senior',
            '5': 'Graduate',
        }
    }

    return render_template('analytics.html', current_user=current_user, data=json.loads(current_user.analytics), options=options)

@auth.route('/signup', methods=['POST'])
def signup_post():
    """
    Handles the "/signup" endpoint on POST request method and responsible for
    storing the creating a new account.
    """

    # Get the full name of the user.
    full_name = request.form.get('full_name').strip()

    # Get the username of the user.
    username = request.form.get('username').strip()

    # Get the email of the user.
    email = request.form.get('email').strip()

    # Get the password of the user.
    password = request.form.get('password').strip()

    # Get the confirmed password of the user.
    c_password = request.form.get('c_password').strip()

    # Get the education level of the user.
    education_level = request.form.get('education_level').strip()

    if full_name == '' or username == '' or email == '' or password == '' or c_password == '' or education_level == '':
        flash('Some fields are empty.')

        return redirect(url_for('auth.signup'))

    # If the passwords doesn't match then send error message.
    if password != c_password:
        flash('Password doesn\'t match.')

        return redirect(url_for('auth.signup'))

    # Search for the user by email in the database.
    user = User.query.filter_by(email=email).first()

    # If the user already exists with that email then send an error message that
    # the email is already taken.
    if user:
        flash('Email address already exists')

        return redirect(url_for('auth.signup'))

    # Search for the user by username in the database.
    user = User.query.filter_by(username=username).first()

    # If the user already exists with that username then send an error message
    # that the username is already taken.
    if user:
        flash('Username already exists.')

        return redirect(url_for('auth.signup'))

    # If everything succeeds, then create a new record for the user in the database.
    new_user = User(full_name=full_name, username=username, email=email, password=generate_password_hash(password, method='sha256'), education_level=education_level)

    # Add the new user to the database.
    db.session.add(new_user)

    # Commit the changes.
    db.session.commit()

    # Finally, redirect the user to the homepage.
    return redirect(url_for('main.index'))

@auth.route('/dashboard')
@login_required
def dashboard():
    """
    Handles the "/dashboard" endpoint.
    """

    return render_template('dashboard.html', current_user=current_user)
