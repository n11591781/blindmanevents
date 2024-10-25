from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    if request.args.get('search') and request.args['search'] != "":
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.title.like(query)))
        return render_template('searchresults.html', events=events)
    else:
        return redirect(url_for('main.index'))

# Changed
@mainbp.route('/event/<int:event_id>')
def view_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404
    return render_template('events/view_event.html', event=event)


@mainbp.route('/profile')
def profile():
    # Render the profile page located in the 'events' folder
    return render_template('events/profile.html')


@mainbp.route('/force-error')
def force_error():
    # This will raise an exception and trigger the 500 error handler
    raise Exception("This is a test 500 error.")


# please
@mainbp.route('/event/<int:event_id>/get-tickets', methods=['GET', 'POST'])
def get_tickets(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404
    
    if request.method == 'POST':
        ticket_quantity = request.form.get('ticket_quantity', type=int)

        # Check if the ticket quantity is valid
        if ticket_quantity and 0 < ticket_quantity <= event.tickets_remaining:
            # Update the database here to reduce the tickets remaining, or process the order
            event.tickets_remaining -= ticket_quantity
            db.session.commit()

            # Redirect to a confirmation page after successful purchase
            return redirect(url_for('main.booking_confirmation', event_id=event_id))
        else:
            # If the quantity is invalid, you could flash a message or show an error
            return "Invalid ticket quantity", 400
    
    return render_template('events/get_tickets.html', event=event)
    

@mainbp.route('/event/<int:event_id>/confirmation')
def booking_confirmation(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return "Event not found", 404
    return render_template('events/booking_confirmation.html', event=event)
