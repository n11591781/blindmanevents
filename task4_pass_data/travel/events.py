from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventdp = Blueprint('destination', __name__, url_prefix='/events')

@eventdp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    organizer_events = db.session.scalars(db.select(Event).where(Event.organizer_id == event.organizer_id)).all()
    form = CommentForm()
    return render_template('events/view_event.html', event=event, organizer_events=organizer_events, form=form)

@eventdp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    # call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(title=form.title.data, date=form.date.data, time=form.time.data, location=form.location.data, event_description=form.event_description.data, image=db_file_path,
    tickets_remaining=form.number_of_tickets.data, status=form.status.data, ticket_price=form.price_of_tickets.data, organizer_id=current_user.id)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    # Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@eventdp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form
      comment = Comment(text=form.text.data, event=event, user=current_user) 
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=id))

@eventdp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    
    # Check if the current user is the organizer of the event
    if event.organizer_id != current_user.id:
        flash("You are not authorized to edit this event", "danger")
        return redirect(url_for('destination.show', id=id))

    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.event_description = form.event_description.data
        event.tickets_remaining = form.number_of_tickets.data
        event.status = form.status.data
        event.ticket_price = form.price_of_tickets.data
        
        # Handle image update
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path

        db.session.commit()
        flash("Event updated successfully", "success")
        return redirect(url_for('destination.show', id=id))

    return render_template('events/edit_event.html', form=form, event=event)
