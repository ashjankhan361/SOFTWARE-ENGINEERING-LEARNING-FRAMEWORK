
from flask_login import UserMixin
from .app import db

class User(UserMixin, db.Model):
    """
    Model for the User.
    """

    # Unique Identifier for the user.
    id = db.Column(db.Integer, primary_key=True)

    # User's full name.
    full_name = db.Column(db.String(100))

    # User handle.
    username = db.Column(db.String(100), unique=True)

    # University email of the user.
    email = db.Column(db.String(100), unique=True)

    # User Password.
    password = db.Column(db.String(100))

    # User's current education level.
    education_level = db.Column(db.String(2))

    # User's phone number.
    phone = db.Column(db.String(15))

    # User's date of birth.
    birthday = db.Column(db.String())

    # User Profile url.
    profile = db.Column(db.String(500))

    # Usage Reminder.
    usage_reminder = db.Column(db.String(100))

    # Analytics as JSON String.
    analytics = db.Column(db.String(2000))
