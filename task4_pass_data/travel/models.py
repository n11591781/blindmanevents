from . import db
from datetime import datetime
from flask_login import UserMixin

# User model, represents a user in the system
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each user
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)  # Unique username
    fname = db.Column(db.String(100), index=True, unique=True, nullable=False)  # First name of the user
    lname = db.Column(db.String(100), index=True, unique=True, nullable=False)  # Last name of the user
    emailid = db.Column(db.String(100), index=True, nullable=False)  # Email address of the user
    street_address = db.Column(db.String(100), index=True, nullable=False)  # User's street address
    contact_info = db.Column(db.String(100), index=True, nullable=False)  # Contact information
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password for security
    joined_on = db.Column(db.DateTime, default=datetime.now())  # Date and time the user joined
    comments = db.relationship('Comment', backref='user')  # Relationship to the user's comments
    booking_history = db.relationship('PurchasedTicket', backref='user')  # Relationship to user's purchased tickets
    booking_history = db.relationship('Event', backref='user')  # Relationship to user's created events
    
    def __repr__(self):
        return f"Name: {self.username}"  # String representation of the user object

# Event model, represents an event in the system
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each event
    title = db.Column(db.String(80))  # Title of the event
    date = db.Column(db.String(80))  # Date of the event
    time = db.Column(db.String(80))  # Time of the event
    location = db.Column(db.String(100))  # Location of the event
    event_description = db.Column(db.String(200))  # Description of the event
    event_type = db.Column(db.String(20))  # Type of event (e.g., concert, festival)
    image = db.Column(db.String(400))  # Image URL or path for the event
    tickets_remaining = db.Column(db.Integer)  # Number of tickets remaining for the event
    status = db.Column(db.String(20))  # Status of the event (e.g., Open, Sold Out, Cancelled)
    ticket_price = db.Column(db.Integer)  # Price per ticket for the event
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ID of the user who organized the event
    comments = db.relationship('Comment', backref='event')  # Relationship to comments on the event
    booking_history = db.relationship('PurchasedTicket', backref='event')  # Relationship to purchased tickets for the event
	
    def __repr__(self):
        return f"Name: {self.title}"  # String representation of the event object

# Comment model, represents a comment on an event
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each comment
    text = db.Column(db.String(400))  # Content of the comment
    created_at = db.Column(db.DateTime, default=datetime.now())  # Date and time the comment was created
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ID of the user who made the comment
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))  # ID of the event the comment is related to

    def __repr__(self):
        return f"Comment: {self.text}"  # String representation of the comment object

# PurchasedTicket model, represents a ticket purchased for an event
class PurchasedTicket(db.Model, UserMixin):
    __tablename__ = 'purchased_tickets'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for each purchased ticket
    ticket_id = db.Column(db.String(100))  # Unique identifier for the ticket
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ID of the user who purchased the ticket
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))  # ID of the event the ticket is for
    booked_on = db.Column(db.DateTime, default=datetime.now())  # Date and time the ticket was booked
    
    def __repr__(self):
        return f"Name: {self.username}"  # String representation of the purchased ticket object
