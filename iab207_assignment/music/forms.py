from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

# Allowed file types for event images
ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

# Form for creating a new event
class EventForm(FlaskForm):
    # Title of the event
    title = StringField('Title', validators=[InputRequired()])
    # Date of the event
    date = StringField('Date', validators=[InputRequired()])
    # Time of the event
    time = StringField('Time', validators=[InputRequired()])
    # Location of the event
    location = StringField('Location', validators=[InputRequired()])
    # Description of the event
    event_description = TextAreaField('Event Description', validators=[InputRequired()])
    # Image upload field with file type restrictions
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'), 
        FileAllowed(ALLOWED_FILE, message='Only PNG or JPG files allowed')
    ])
    # Number of tickets available for the event
    tickets_remaining = StringField('Number of Tickets', validators=[InputRequired()])
    # Price of the tickets
    ticket_price = StringField('Price of Tickets', validators=[InputRequired()])
    # Status of the event (e.g., Open, Cancelled)
    status = StringField('Status', validators=[InputRequired()])
    # Type of the event (e.g., LiveJazz, TributeShow)
    event_type = StringField('Type of Event', validators=[InputRequired()])
    # Submit button for creating the event
    submit = SubmitField("Create")
    
# Form for user login
class LoginForm(FlaskForm):
    # Username field for login
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    # Password field for login
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    # Submit button for logging in
    submit = SubmitField("Login")

# Form for user registration
class RegisterForm(FlaskForm):
    # Username field for registration
    user_name = StringField("User Name", validators=[InputRequired()])
    # Email field with validation for proper email format
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    # Additional fields for user information
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    street_address = StringField("Street Address", validators=[InputRequired()])
    contact_number = StringField("Contact Number", validators=[InputRequired()])
    
    # Password field with confirmation for matching passwords
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    # Confirm password field
    confirm = PasswordField("Confirm Password")
    
    # Submit button for registering
    submit = SubmitField("Register")

# Form for adding a comment
class CommentForm(FlaskForm):
    # Text area for the comment content
    text = TextAreaField('Comment', [InputRequired()])
    # Submit button to post the comment
    submit = SubmitField('Create')
