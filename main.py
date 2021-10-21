
# Import required packages.
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .app import db

# Initialize the Main Blueprint.
# This blueprint defines the routes that can be accessed by anyone.
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Handles the Homepage or "/" endpoint.
    """

    # Redirect the user to the dashboard if already logged in.
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    return render_template('index.html')

@main.route('/robots.txt')
@main.route('/sitemap.xml')
def sitemap():
    """
    Handle the robots.txt and sitemap.xml which are for the Google Bot,
    Bing Bot, Baidu Bot, etc. for SEO (Search Engine Optimization) purpose.
    """

    # Returns the contents of the requested files as is.
    return send_from_directory(app.static_folder, request.path[1:])
