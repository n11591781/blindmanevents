from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

# Create new destination
class EventForm(FlaskForm):
  title = StringField('Title', validators=[InputRequired()])
  date = StringField('Date', validators=[InputRequired()])
  time = StringField('Time', validators=[InputRequired()])
  location = StringField('Location', validators=[InputRequired()])
  event_description = TextAreaField('Event Description', validators = [InputRequired()])
  image = FileField('Destination Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only PNG or JPG files allowed')])
  number_of_tickets = StringField('Number of Tickets', validators=[InputRequired()])
  price_of_tickets = StringField('Price of Tickets', validators=[InputRequired()])
  status = StringField('Status', validators=[InputRequired()])
  submit = SubmitField("Create")
    
# User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')