from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event, PurchasedTicket, User
from . import db
from flask_login import login_required, current_user

# Define a blueprint for main routes
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    # Fetch all events from the database to display on the homepage
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    # Handle search functionality
    if request.args.get('search') and request.args['search'] != "":
        query = "%" + request.args['search'] + "%"  # Create a query with wildcards for partial matches
        events = db.session.scalars(db.select(Event).where(Event.title.like(query)))  # Search events by title
        return render_template('searchresults.html', events=events)
    else:
        # Redirect to homepage if search query is empty
        return redirect(url_for('main.index'))

@mainbp.route('/<category>')
def category_view(category):
    # Display events filtered by category
    events = db.session.scalars(db.select(Event).where(Event.event_type == category))
    return render_template('searchresults.html', events=events)

@mainbp.route('/event/<int:event_id>')
def view_event(event_id):
    # View details of a specific event by ID
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404  # Return a 404 error if the event doesn't exist
    return render_template('events/view_event.html', event=event, organizer_username=event.user.username)

@mainbp.route('/profile')
@login_required
def profile():
    # Display the user's profile, including booked events
    user = db.session.get(User, current_user.id)
    booked_events = db.session.scalars(db.select(PurchasedTicket).where(PurchasedTicket.user_id==current_user.id)).all()
    return render_template('events/profile.html', user=user, booked_events=booked_events)

@mainbp.route('/force-error')
def force_error():
    # Test route to trigger a 500 error for error handling demonstration
    raise Exception("This is a test 500 error.")

@mainbp.route('/event/<int:event_id>/get-tickets', methods=['GET', 'POST'])
@login_required
def get_tickets(event_id):
    # Route to purchase tickets for an event
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404  # Return a 404 error if the event doesn't exist
    
    if request.method == 'POST':
        # Process ticket purchase on form submission
        ticket_quantity = request.form.get('ticket_quantity', type=int)

        # Check if the requested ticket quantity is valid
        if ticket_quantity and 0 < ticket_quantity <= event.tickets_remaining:
            # Create tickets and update event tickets remaining
            for ticket in range(ticket_quantity):
                ticket_identifier = f"{event.title[:5]}{event.tickets_remaining}"
                purchased_ticket = PurchasedTicket(ticket_id=ticket_identifier, user_id=current_user.id, event_id=event.id)
                event.tickets_remaining -= 1
                db.session.add(purchased_ticket)
            db.session.commit()  # Save changes to the database
            # Redirect to confirmation page after purchase
            return redirect(url_for('main.booking_confirmation', event_id=event_id))
        else:
            # If ticket quantity is invalid, return an error
            return "Invalid ticket quantity", 400
    
    # Render the ticket purchase form if GET request
    return render_template('events/get_tickets.html', event=event)

@mainbp.route('/event/<int:event_id>/confirmation')
@login_required
def booking_confirmation(event_id):
    # Display the booking confirmation page
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404  # Return 404 if event is not found

    # Retrieve the user's most recent booking for this event
    booking = db.session.scalars(
        db.select(PurchasedTicket).where(
            PurchasedTicket.event_id == event_id,
            PurchasedTicket.user_id == current_user.id
        )
    ).first()  # Get only the first booking (adjust if multiple allowed)

    if booking is None:
        return "Booking not found", 404  # Return 404 if no booking found

    # Render confirmation page with event and booking information
    return render_template('events/booking_confirmation.html', event=event, booking_id=booking.id)
