from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    fname = db.Column(db.String(100), index=True, unique=True, nullable=False)
    lname = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    street_address = db.Column(db.String(100), index=True, nullable=False)
    contact_info = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    joined_on = db.Column(db.DateTime, default=datetime.now())
    comments = db.relationship('Comment', backref='user')
    booking_history = db.relationship('PurchasedTicket', backref='user')
    booking_history = db.relationship('Event', backref='user')
    
    def __repr__(self):
        return f"Name: {self.username}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    location = db.Column(db.String(100))
    event_description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    tickets_remaining = db.Column(db.Integer)
    status = db.Column(db.String(20))
    ticket_price = db.Column(db.Integer)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')
    booking_history = db.relationship('PurchasedTicket', backref='event')
	
    def __repr__(self):
        return f"Name: {self.title}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class PurchasedTicket(db.Model, UserMixin):
    __tablename__ = 'purchased_tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booked_on = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return f"Name: {self.username}"