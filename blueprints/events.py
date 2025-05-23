from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Event, EventAttendee, Alumni
from forms.events import EventForm, EventRegistrationForm
from extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os

events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/')
def index():
    # Get query parameters
    view = request.args.get('view', 'list')  # list or calendar
    
    # Get upcoming and past events
    upcoming_events = Event.query.filter(Event.date >= datetime.utcnow()).order_by(Event.date).all()
    past_events = Event.query.filter(Event.date < datetime.utcnow()).order_by(Event.date.desc()).all()
    
    return render_template('events/index.html', 
                          upcoming_events=upcoming_events,
                          past_events=past_events,
                          view=view)

@events.route('/<int:event_id>')
def detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if user is registered
    is_registered = False
    if current_user.is_authenticated and not current_user.is_admin:
        alumni = Alumni.query.filter_by(user_id=current_user.id).first()
        if alumni:
            registration = EventAttendee.query.filter_by(event_id=event.id, alumni_id=alumni.id).first()
            is_registered = registration is not None
    
    # Get attendees
    attendees = EventAttendee.query.filter_by(event_id=event.id).join(Alumni).all()
    
    # Registration form
    form = EventRegistrationForm()
    
    return render_template('events/detail.html', 
                          event=event,
                          is_registered=is_registered,
                          attendees=attendees,
                          form=form)

@events.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register(event_id):
    if current_user.is_admin:
        flash('Admins cannot register for events.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    event = Event.query.get_or_404(event_id)
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()
    
    # Check if already registered
    existing_registration = EventAttendee.query.filter_by(event_id=event.id, alumni_id=alumni.id).first()
    if existing_registration:
        flash('You are already registered for this event.', 'info')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Check if event is in the past
    if event.is_past:
        flash('Cannot register for past events.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Register for event
    registration = EventAttendee(
        event_id=event.id,
        alumni_id=alumni.id,
        status='registered'
    )
    db.session.add(registration)
    db.session.commit()
    
    flash('You have successfully registered for this event!', 'success')
    return redirect(url_for('events.detail', event_id=event_id))

@events.route('/<int:event_id>/cancel', methods=['POST'])
@login_required
def cancel_registration(event_id):
    if current_user.is_admin:
        flash('Admins cannot cancel event registrations.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    event = Event.query.get_or_404(event_id)
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()
    
    # Find registration
    registration = EventAttendee.query.filter_by(event_id=event.id, alumni_id=alumni.id).first()
    if not registration:
        flash('You are not registered for this event.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Check if event is in the past
    if event.is_past:
        flash('Cannot cancel registration for past events.', 'warning')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Cancel registration
    db.session.delete(registration)
    db.session.commit()
    
    flash('Your registration has been cancelled.', 'success')
    return redirect(url_for('events.detail', event_id=event_id))

@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin:
        flash('Only admins can create events.', 'warning')
        return redirect(url_for('events.index'))
    
    form = EventForm()
    if form.validate_on_submit():
        # Create new event
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            end_date=form.end_date.data,
            location=form.location.data,
            is_virtual=form.is_virtual.data,
            virtual_link=form.virtual_link.data if form.is_virtual.data else None,
            created_by=current_user.id
        )
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # TODO: Save file and update image field
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
    
    return render_template('events/create.html', form=form)

@events.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    if not current_user.is_admin:
        flash('Only admins can edit events.', 'warning')
        return redirect(url_for('events.index'))
    
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        # Update event
        form.populate_obj(event)
        
        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # TODO: Save file and update image field
        
        db.session.commit()
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event.id))
    
    return render_template('events/edit.html', form=form, event=event)
