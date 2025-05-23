from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Alumni, User, Event, EventAttendee
from forms.alumni import ProfileForm
from extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

alumni = Blueprint('alumni', __name__)

@alumni.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    # Get alumni profile
    alumni_profile = Alumni.query.filter_by(user_id=current_user.id).first()
    
    # Get upcoming events
    upcoming_events = Event.query.filter(Event.date >= datetime.utcnow()).order_by(Event.date).limit(3).all()
    
    # Get registered events
    registered_events = EventAttendee.query.filter_by(alumni_id=alumni_profile.id).join(Event).all()
    
    # Calculate profile completeness
    profile_completeness = calculate_profile_completeness(alumni_profile)
    
    return render_template('alumni/dashboard.html', 
                          alumni=alumni_profile,
                          upcoming_events=upcoming_events,
                          registered_events=registered_events,
                          profile_completeness=profile_completeness)

@alumni.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    
    alumni_profile = Alumni.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm(obj=alumni_profile)
    
    if form.validate_on_submit():
        # Update alumni profile
        form.populate_obj(alumni_profile)
        
        # Handle profile photo upload
        if form.profile_photo.data:
            filename = secure_filename(form.profile_photo.data.filename)
            # TODO: Save file and update profile_photo field
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('alumni.profile'))
    
    return render_template('alumni/profile.html', form=form, alumni=alumni_profile)

@alumni.route('/directory')
@login_required
def directory():
    # Get query parameters
    faculty = request.args.get('faculty')
    department = request.args.get('department')
    graduation_year = request.args.get('graduation_year')
    search = request.args.get('search')
    
    # Base query
    query = Alumni.query
    
    # Apply filters
    if faculty:
        query = query.filter_by(faculty=faculty)
    if department:
        query = query.filter_by(department=department)
    if graduation_year:
        query = query.filter_by(graduation_year=graduation_year)
    if search:
        query = query.filter(
            (Alumni.first_name.like(f'%{search}%')) |
            (Alumni.last_name.like(f'%{search}%')) |
            (Alumni.matriculation_number.like(f'%{search}%'))
        )
    
    # Get results
    alumni_list = query.all()
    
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()
    
    
    # Get unique faculties, departments, and graduation years for filters
    faculties = db.session.query(Alumni.faculty).distinct().all()
    departments = db.session.query(Alumni.department).distinct().all()
    graduation_years = db.session.query(Alumni.graduation_year).distinct().order_by(Alumni.graduation_year.desc()).all()
    
    return render_template('alumni/directory.html', 
                            alumni = alumni,
                          alumni_list=alumni_list,
                          faculties=faculties,
                          departments=departments,
                          graduation_years=graduation_years)

def calculate_profile_completeness(alumni):
    """Calculate profile completeness percentage"""
    fields = [
        alumni.first_name, alumni.last_name, alumni.phone,
        alumni.date_of_birth, alumni.profile_photo, alumni.bio,
        alumni.matriculation_number, alumni.faculty, alumni.department,
        alumni.graduation_year, alumni.degree, alumni.job_title,
        alumni.organization, alumni.industry, alumni.linkedin_url
    ]
    
    filled_fields = sum(1 for field in fields if field)
    return int((filled_fields / len(fields)) * 100)
