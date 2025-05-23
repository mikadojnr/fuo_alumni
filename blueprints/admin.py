from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Alumni, Event, Project, Contribution, EventAttendee, Announcement
from forms.admin import AnnouncementForm, EventForm, ProjectForm, ProfileForm, SettingsForm, ContributionForm, UserForm
import os
from datetime import datetime
from sqlalchemy import desc, func
from utils.decorators import admin_required
import uuid

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function for saving uploaded files
def save_file(file, folder):
    if not file:
        return None

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Full path to save the file
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    file_path = os.path.join(upload_dir, unique_filename)

    # Ensure the directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Save the file
    file.save(file_path)

    # Return the path relative to the static folder for use in templates
    return f"/static/img/{folder}/{unique_filename}"

# Dashboard
@admin.route('/')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    user_count = User.query.count()
    alumni_count = Alumni.query.count()
    event_count = Event.query.count()
    project_count = Project.query.count()
    contribution_count = Contribution.query.count()
    
    # Get recent events
    recent_events = Event.query.order_by(desc(Event.created_at)).limit(5).all()
    
    # Get active projects
    active_projects = Project.query.filter_by(is_active=True).order_by(desc(Project.created_at)).limit(5).all()
    
    # Get recent contributions
    recent_contributions = Contribution.query.order_by(desc(Contribution.created_at)).limit(5).all()
    
    contribution_total = db.session.query(func.coalesce(func.sum(Contribution.amount), 0)).scalar()

    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          alumni_count=alumni_count,
                          event_count=event_count,
                          project_count=project_count,
                          contribution_count=contribution_count,
                          recent_events=recent_events,
                          active_projects=active_projects,
                          recent_contributions=recent_contributions,
                          contribution_total=contribution_total)

# Event Management Routes
@admin.route('/events')
@login_required
@admin_required
def events():
    events = Event.query.order_by(desc(Event.date)).all()
    now = datetime.utcnow()
    return render_template(
        'admin/events/index.html', 
        events=events,
        now=now
        )

@admin.route('/events/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        # Handle image upload
        image_path = None
        if form.image.data:
            image_path = save_file(form.image.data, 'events')
        
        # Create new event
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            end_date=form.end_date.data,
            location=form.location.data if not form.is_virtual.data else None,
            is_virtual=form.is_virtual.data,
            virtual_link=form.virtual_link.data if form.is_virtual.data else None,
            image=image_path,
            created_by=current_user.id,
            created_at=datetime.now()
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/events/create.html', form=form)

@admin.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    
    
    if form.validate_on_submit():
        # Handle image upload
        if form.image.data:
            # Delete old image if it exists
            if event.image and os.path.exists(os.path.join(current_app.root_path, 'static', event.image.lstrip('/'))):
                os.remove(os.path.join(current_app.root_path, 'static', event.image.lstrip('/')))
            
            image_path = save_file(form.image.data, 'events')
            event.image = image_path
        
        # Update event details
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.end_date = form.end_date.data
        event.is_virtual = form.is_virtual.data
        
        if form.is_virtual.data:
            event.location = None
            event.virtual_link = form.virtual_link.data
        else:
            event.location = form.location.data
            event.virtual_link = None
        
        db.session.commit()
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/events/edit.html', form=form, event=event)

@admin.route('/events/<int:event_id>/view')
@login_required
@admin_required
def view_event(event_id):
    now = datetime.utcnow()
    event = Event.query.get_or_404(event_id)
    attendees = EventAttendee.query.filter_by(event_id=event_id).all()
    return render_template('admin/events/view.html', event=event, attendees=attendees, now=now)

@admin.route('/events/<int:event_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Instead of deleting, we could add a 'status' field to mark as cancelled
    # For now, we'll just delete the event
    db.session.delete(event)
    db.session.commit()
    
    flash('Event cancelled successfully!', 'success')
    return redirect(url_for('admin.events'))


# Project Management Routes
@admin.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.order_by(desc(Project.created_at)).all()
    now = datetime.now()
    return render_template('admin/projects/index.html', projects=projects, now=now)

@admin.route('/projects/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_project():
    form = ProjectForm()
    
    if form.validate_on_submit():
        # Handle image upload
        image_path = None
        if form.image.data:
            image_path = save_file(form.image.data, 'projects')
        
        # Create new project
        new_project = Project(
            title=form.title.data,
            description=form.description.data,
            goal_amount=form.goal_amount.data,
            image=image_path,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_active=True,  # New projects are active by default
            created_by=current_user.id,
            created_at=datetime.now()
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/projects/create.html', form=form)

@admin.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        # Handle image upload
        if form.image.data:
            if project.image:
                old_image_path = os.path.join(current_app.root_path, 'static', project.image.lstrip('/'))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            image_path = save_file(form.image.data, 'projects')
            project.image = image_path

        # Update fields from form
        project.title = form.title.data
        project.description = form.description.data
        project.goal_amount = form.goal_amount.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.is_active = form.is_active.data

        db.session.commit()

        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/projects/edit.html', form=form, project=project)

@admin.route('/projects/<int:project_id>/view')
@login_required
@admin_required
def project_view(project_id):
    project = Project.query.get_or_404(project_id)
    contributions = Contribution.query.filter_by(project_id=project_id).order_by(desc(Contribution.created_at)).all()
    now = datetime.utcnow()
    return render_template('admin/projects/view.html', project=project, contributions=contributions, now=now)

@admin.route('/projects/<int:project_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Mark project as inactive instead of deleting
    project.is_active = False
    db.session.commit()
    
    flash('Project cancelled successfully!', 'success')
    return redirect(url_for('admin.projects'))

@admin.route('/projects/<int:project_id>/end', methods=['POST'])
@login_required
@admin_required
def end_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Mark project as completed by setting end_date to today
    project.end_date = datetime.now().date()
    project.is_active = False
    db.session.commit()
    
    flash('Project marked as completed!', 'success')
    return redirect(url_for('admin.projects'))

# User Management Routes
@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)

@admin.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def user_create():
    form = UserForm()
    
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return render_template('admin/users/create.html', form=form)
        
        # Create new user
        new_user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            is_active=form.is_active.data,
            is_admin=form.is_admin.data,
            created_at=datetime.now(),
            email_verified=True  # Admin-created users are verified by default
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # If user is admin, create admin record
        if form.is_admin.data:
            admin = Admin(
                user_id=new_user.id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                role=form.role.data if form.role.data else 'Staff'
            )
            db.session.add(admin)
            db.session.commit()
        
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/create.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    # Pre-fill admin data if user is admin
    if user.is_admin and user.admin:
        form.first_name.data = user.admin.first_name
        form.last_name.data = user.admin.last_name
        form.role.data = user.admin.role
    
    if form.validate_on_submit():
        # Update user details
        user.email = form.email.data
        user.is_active = form.is_active.data
        
        # Only update password if provided
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        
        # Handle admin status change
        if form.is_admin.data != user.is_admin:
            user.is_admin = form.is_admin.data
            
            # If user is now admin but wasn't before, create admin record
            if form.is_admin.data and not user.admin:
                admin = Admin(
                    user_id=user.id,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    role=form.role.data if form.role.data else 'Staff'
                )
                db.session.add(admin)
            
            # If user is no longer admin but was before, delete admin record
            elif not form.is_admin.data and user.admin:
                db.session.delete(user.admin)
        
        # Update admin details if user is admin
        elif form.is_admin.data and user.admin:
            user.admin.first_name = form.first_name.data
            user.admin.last_name = form.last_name.data
            user.admin.role = form.role.data
        
        db.session.commit()
        
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/edit.html', form=form, user=user)

@admin.route('/users/<int:user_id>/view')
@login_required
@admin_required
def user_view(user_id):
    user = User.query.get_or_404(user_id)

    # Preload contributions and events if available
    contributions = []
    total_amount = 0
    events_attended = []

    if user.alumni:
        contributions = user.alumni.contributions.all()
        total_amount = sum(c.amount for c in contributions)
        events_attended = user.alumni.events.all()

    return render_template(
        'admin/users/view.html',
        user=user,
        contributions=contributions,
        total_contributions_amount=total_amount,
        events_attended=events_attended,
    )

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

# Contribution Management Routes
@admin.route('/contributions')
@login_required
@admin_required
def contributions():
    contributions = Contribution.query.order_by(desc(Contribution.created_at)).all()
    projects = Project.query.all()
    return render_template('admin/contributions/index.html', contributions=contributions, projects=projects)

@admin.route('/contributions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def contribution_create():
    form = ContributionForm()
    
    # Populate alumni and project choices
    form.alumni_id.choices = [(a.id, f"{a.full_name} ({a.user.email})") for a in Alumni.query.all()]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.filter_by(is_active=True).all()]
    
    if form.validate_on_submit():
        # Create new contribution
        new_contribution = Contribution(
            alumni_id=form.alumni_id.data,
            project_id=form.project_id.data,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            transaction_id=form.transaction_id.data,
            is_anonymous=form.is_anonymous.data,
            dedication=form.dedication.data,
            created_at=datetime.now()
        )
        
        db.session.add(new_contribution)
        
        # Update project current amount
        project = Project.query.get(form.project_id.data)
        project.current_amount += form.amount.data
        
        db.session.commit()
        
        flash('Contribution added successfully!', 'success')
        return redirect(url_for('admin.contributions'))
    
    return render_template('admin/contributions/create.html', form=form)

@admin.route('/contributions/<int:contribution_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def contribution_edit(contribution_id):
    contribution = Contribution.query.get_or_404(contribution_id)
    form = ContributionForm(obj=contribution)
    
    # Populate alumni and project choices
    form.alumni_id.choices = [(a.id, f"{a.full_name} ({a.user.email})") for a in Alumni.query.all()]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.all()]
    
    if form.validate_on_submit():
        # Store old amount and project for updating
        old_amount = contribution.amount
        old_project_id = contribution.project_id
        
        # Update contribution details
        contribution.alumni_id = form.alumni_id.data
        contribution.project_id = form.project_id.data
        contribution.amount = form.amount.data
        contribution.payment_method = form.payment_method.data
        contribution.transaction_id = form.transaction_id.data
        contribution.is_anonymous = form.is_anonymous.data
        contribution.dedication = form.dedication.data
        
        # Update project amounts if needed
        if old_project_id != form.project_id.data:
            # Subtract from old project
            old_project = Project.query.get(old_project_id)
            old_project.current_amount -= old_amount
            
            # Add to new project
            new_project = Project.query.get(form.project_id.data)
            new_project.current_amount += form.amount.data
        elif old_amount != form.amount.data:
            # Just update the amount difference
            project = Project.query.get(form.project_id.data)
            project.current_amount = project.current_amount - old_amount + form.amount.data
        
        db.session.commit()
        
        flash('Contribution updated successfully!', 'success')
        return redirect(url_for('admin.contributions'))
    
    return render_template('admin/contributions/edit.html', form=form, contribution=contribution)

@admin.route('/contributions/<int:contribution_id>/view')
@login_required
@admin_required
def contribution_view(contribution_id):
    contribution = Contribution.query.get_or_404(contribution_id)
    return render_template('admin/contributions/view.html', contribution=contribution)

@admin.route('/contributions/<int:contribution_id>/delete', methods=['POST'])
@login_required
@admin_required
def contribution_delete(contribution_id):
    contribution = Contribution.query.get_or_404(contribution_id)
    
    # Update project amount
    project = Project.query.get(contribution.project_id)
    project.current_amount -= contribution.amount
    
    db.session.delete(contribution)
    db.session.commit()
    
    flash('Contribution deleted successfully!', 'success')
    return redirect(url_for('admin.contributions'))

# Alumni Management Routes
@admin.route('/alumni')
@login_required
@admin_required
def alumni():
    alumni = Alumni.query.all()
    return render_template('admin/alumni/index.html', alumni=alumni)

@admin.route('/alumni/<int:alumni_id>')
@login_required
@admin_required
def alumni_detail(alumni_id):
    alumni = Alumni.query.get_or_404(alumni_id)
    return render_template('admin/alumni/view.html', alumni=alumni)


# Settings and Profile Routes
@admin.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    form = SettingsForm()
    
    if form.validate_on_submit():
        # Update system settings
        # This would typically update a settings table or config file
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', form=form)

@admin.route('/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def profile():
    admin = current_user.admin
    form = ProfileForm(obj=admin)
    
    if form.validate_on_submit():
        # Update admin profile
        admin.first_name = form.first_name.data
        admin.last_name = form.last_name.data
        
        # Update password if provided
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    
    return render_template('admin/profile.html', form=form, admin=admin)


# Announcement Management Routes
@admin.route('/announcements')
@login_required
@admin_required
def announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements/index.html', announcements=announcements)

@admin.route('/announcements/create', methods=['GET', 'POST'])
@login_required
@admin_required
def announcement_create():
    # Check if we're editing an existing announcement
    announcement_id = request.args.get('announcement_id', type=int)
    announcement = None
    if announcement_id:
        announcement = Announcement.query.get_or_404(announcement_id)
    
    # Create form and populate with announcement data if editing
    form = AnnouncementForm(obj=announcement)
    
    # Set page title based on whether we're creating or editing
    page_title = "Edit Announcement" if announcement else "Create Announcement"
    
    if form.validate_on_submit():
        if announcement:
            # Update existing announcement
            announcement.title = form.title.data
            announcement.content = form.content.data
            announcement.is_active = form.is_active.data
            announcement.updated_at = datetime.now()
            
            db.session.commit()
            flash('Announcement updated successfully!', 'success')
        else:
            # Create new announcement
            new_announcement = Announcement(
                title=form.title.data,
                content=form.content.data,
                is_active=form.is_active.data,
                created_by=current_user.id,
                created_at=datetime.now()
            )
            
            db.session.add(new_announcement)
            db.session.commit()
            flash('Announcement created successfully!', 'success')
        
        return redirect(url_for('admin.announcements'))
    
    return render_template('admin/announcements/create.html', form=form, announcement=announcement, page_title=page_title)

@admin.route('/announcements/<int:announcement_id>')
@login_required
@admin_required
def announcement_view(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('admin/announcements/view.html', announcement=announcement)

@admin.route('/announcements/<int:announcement_id>/edit')
@login_required
@admin_required
def announcement_edit(announcement_id):
    # Redirect to create with announcement_id as query parameter
    return redirect(url_for('admin.announcement_create', announcement_id=announcement_id))

@admin.route('/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
@admin_required
def announcement_delete(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    
    db.session.delete(announcement)
    db.session.commit()
    
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('admin.announcements'))
