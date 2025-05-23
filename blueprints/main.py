from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from models import Event, Announcement, Project
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get upcoming events
    upcoming_events = Event.query.filter(Event.date >= datetime.utcnow()).order_by(Event.date).limit(3).all()
    
    # Get latest announcements
    announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).limit(3).all()
    
    # Get featured projects
    featured_projects = Project.query.filter_by(is_active=True).order_by(Project.created_at.desc()).limit(3).all()
    
    return render_template('index.html', 
                          upcoming_events=upcoming_events,
                          announcements=announcements,
                          featured_projects=featured_projects)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
