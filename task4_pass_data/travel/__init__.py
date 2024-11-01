from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

# Initialize SQLAlchemy for database management
db = SQLAlchemy()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Use Bootstrap5 for easy styling of forms and components
    Bootstrap5(app)

    # Set up Bcrypt for secure password hashing
    Bcrypt(app)

    # Secret key for session management (suggest using environment variable in production)
    app.secret_key = 'somerandomvalue'

    # Configure the database URI for SQLite and initialize the database with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmdb.sqlite'
    db.init_app(app)

    # Set the upload folder path for event images
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # Set up the login manager for handling user sessions
    login_manager = LoginManager()
    # Redirect users to 'auth.login' page if not authenticated
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader function required by Flask-Login to manage user sessions
    from .models import User  # Import User model here to prevent circular imports
    @login_manager.user_loader
    def load_user(user_id):
        # Return user object by querying the database with user_id
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # Register blueprints for modular routing
    from . import views  # Import main views
    app.register_blueprint(views.mainbp)
    from . import events  # Import event-specific views
    app.register_blueprint(events.eventdp)
    from .auth import authbp  # Import authentication views
    app.register_blueprint(authbp, url_prefix='/auth')  

    # Error handling for 404 Not Found
    @app.errorhandler(404)
    def not_found(e):
        # Render custom 404 error page
        return render_template("404.html", error=e), 404

    # Error handling for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_error(e):
        # Render custom 500 error page
        return render_template("500.html", error=e), 500

    # Context processor to inject the current year into all templates
    @app.context_processor
    def get_context():
        # Pass the current year to templates for display in the footer or other sections
        year = datetime.datetime.today().year
        return dict(year=year)

    # Return the Flask app instance
    return app
