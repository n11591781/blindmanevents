from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint for authentication-related routes
authbp = Blueprint('auth', __name__ )

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    # Instantiate the registration form
    register = RegisterForm()
    # Check if the form is valid and the HTTP request is POST
    if register.validate_on_submit():
        # Retrieve user details from the form
        uname = register.user_name.data
        fname = register.first_name.data
        lname = register.last_name.data
        email = register.email_id.data
        address = register.street_address.data
        phone = register.contact_number.data
        pwd = register.password.data
        
        # Check if a user with the same username already exists in the database
        user = db.session.scalar(db.select(User).where(User.username == uname))
        
        if user:  # If user exists, flash an error message and redirect to register page
            flash('Username already exists, please try another')
            return redirect(url_for('authbp.register'))
        
        # Hash the password before storing it in the database
        pwd_hash = generate_password_hash(pwd)
        
        # Create a new User model object with the provided details
        new_user = User(
            username=uname, fname=fname, lname=lname, emailid=email, 
            street_address=address, contact_info=phone, password_hash=pwd_hash
        )
        # Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to the home page after successful registration
        return redirect(url_for('main.index'))
    else:
        # Render the registration form template with heading 'Register'
        return render_template('user.html', form=register, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    # Instantiate the login form
    login_form = LoginForm()
    error = None  # Initialize error variable to track login issues
    if(login_form.validate_on_submit() == True):
        # Get the username and password from the form
        user_name = login_form.user_name.data
        password = login_form.password.data
        # Query the database for a user with the entered username
        user = db.session.scalar(db.select(User).where(User.username == user_name))
        
        # Check if the user exists and the password is correct
        if user is None:
            error = 'Incorrect username'  # Security note: giving detailed errors may be a risk
        elif not check_password_hash(user.password_hash, password):  # Verify password hash
            error = 'Incorrect password'
        
        # If no errors, log the user in and redirect to the home page
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            # Flash the error message if username/password is incorrect
            flash(error)
    # Render the login form template with heading 'Login'
    return render_template('user.html', form=login_form, heading='Login')

# Duplicate blueprint instance for authentication (remove if unused)
auth = Blueprint('auth', __name__)

@auth.route('/logout')
@login_required
def logout():
    # Log the user out and flash a success message
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@authbp.route('/logout')
@login_required
def logout():
    # Log the user out and redirect to the home page
    logout_user()
    return redirect(url_for('main.index'))
