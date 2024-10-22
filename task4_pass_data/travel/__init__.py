from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # we use this utility module to display forms quickly
    Bootstrap5(app)

    # this is a much safer way to store passwords
    Bcrypt(app)

    # a secret key for the session object
    # (it would be better to use an environment variable here)
    app.secret_key = 'somerandomvalue'

    # Configure and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bmdb.sqlite'
    db.init_app(app)

    # config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function that takes user_id and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.eventdp)
    from .auth import authbp  
    app.register_blueprint(authbp, url_prefix='/auth')  

    # Error handling for 404 and 500 errors
    @app.errorhandler(404)
    def not_found(e):
        # 404 Page Not Found
        return render_template("404.html", error=e), 404

    @app.errorhandler(500)
    def internal_error(e):
        # 500 Internal Server Error
        return render_template("500.html", error=e), 500

    # Context processor to pass the current year to all templates
    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    return app
