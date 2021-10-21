
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the SQLAlchemy.
db = SQLAlchemy()

def create_app():
    # Initialize the Flask app.
    app = Flask(__name__)

    # Set the app secret and database path.
    app.config['SECRET_KEY'] = 'AE5A3B321785C4C53124F2F2E6AD1'

    if os.getenv('SELF_FRAMEWORK_TESTING', 'False') == 'True':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.sqlite'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Register blueprints for authorized routes.
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Register blueprints for non-authorized routes.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Run the following code to define schema
# from se_framework import db, create_app
# db.create_all(app=create_app())


# from se_framework.app import create_app, db
# os.environ["SELF_FRAMEWORK_TESTING"] = "True"

