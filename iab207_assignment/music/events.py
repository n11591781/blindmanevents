from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

# Define a blueprint for event-related routes with a URL prefix '/events'
eventdp = Blueprint('event', __name__, url_prefix='/events')

@eventdp.route('/<id>')
def show(id):
    # Fetch the event by ID from the database
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        # Return a 404 error if event is not found
        abort(404)
    
    # Retrieve other events organized by the same user
    organizer_events = db.session.scalars(db.select(Event).where(Event.organizer_id == event.organizer_id)).all()
    
    # Initialize a comment form for the event
    form = CommentForm()
    
    # Render the event detail page with the event data, organizer's other events, and the comment form
    return render_template('events/view_event.html', event=event, organizer_events=organizer_events, form=form)

@eventdp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Endpoint for creating a new event, accessible only by logged-in users
    print('Method type: ', request.method)  # Debugging: print request method type
    form = EventForm()
    
    # Check if form data is valid on submission
    if form.validate_on_submit():
        # Handle file upload for the event image and get the file path
        db_file_path = check_upload_file(form)
        
        # Create a new Event object with form data and set the organizer to the current user
        event = Event(
            title=form.title.data, 
            date=form.date.data, 
            time=form.time.data, 
            location=form.location.data, 
            event_description=form.event_description.data, 
            image=db_file_path,
            tickets_remaining=form.tickets_remaining.data, 
            status=form.status.data, 
            ticket_price=form.ticket_price.data, 
            organizer_id=current_user.id,
            event_type=form.event_type.data
        )
        
        # Add the event to the database session and commit it
        db.session.add(event)
        db.session.commit()
        
        # Flash success message and redirect to the event creation page
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
    
    # Render the event creation form if the request is GET or form validation fails
    return render_template('events/create.html', form=form)

def check_upload_file(form):
    # Handle the image file upload for an event
    fp = form.image.data  # Access the uploaded file
    filename = fp.filename  # Get the filename
    
    # Define the base path and upload path for saving the file
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    
    # Define the relative path for database storage (for use in HTML)
    db_upload_path = '/static/image/' + secure_filename(filename)
    
    # Save the file at the specified upload path and return the database path
    fp.save(upload_path)
    return db_upload_path

@eventdp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    # Endpoint to add a comment to a specific event, restricted to logged-in users
    form = CommentForm()
    
    # Fetch the event associated with the comment by its ID
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
    # Check if the form submission is valid
    if form.validate_on_submit():
        # Create a Comment object with the comment text, event, and current user
        comment = Comment(text=form.text.data, event=event, user=current_user)
        
        # Add the comment to the database and commit it
        db.session.add(comment)
        db.session.commit()
        
        # Flash success message and redirect to the event page
        flash('Your comment has been added', 'success')
    
    # Redirect to the event's detail page after adding the comment
    return redirect(url_for('event.show', id=id))

@eventdp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    # Endpoint to edit an existing event, restricted to the event organizer
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        # Return a 404 error if event is not found
        abort(404)
    
    # Check if the current user is the organizer of the event
    if event.organizer_id != current_user.id:
        flash("You are not authorized to edit this event", "danger")
        return redirect(url_for('event.show', id=id))
    
    # Initialize the form with existing event data
    form = EventForm(obj=event)
    
    # Update the event details if form is valid on submission
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.event_description = form.event_description.data
        event.tickets_remaining = form.tickets_remaining.data
        event.status = form.status.data
        event.ticket_price = form.ticket_price.data
        event.event_type = form.event_type.data
        
        # Check if a new image is uploaded and update it
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path
        
        # Commit the updated event data to the database
        db.session.commit()
        flash("Event updated successfully", "success")
        
        # Redirect to the event's detail page after updating
        return redirect(url_for('event.show', id=id))
    
    # Render the event edit form if request is GET or form validation fails
    return render_template('events/edit_event.html', form=form, event=event)
