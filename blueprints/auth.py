from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Alumni, Admin
from forms.auth import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from extensions import db
import secrets
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.email_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('alumni.dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please login or use a different email.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if matriculation number already exists
        if Alumni.query.filter_by(matriculation_number=form.matriculation_number.data).first():
            flash('Matriculation number already registered. Please contact support if this is an error.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(
            email=form.email.data,
            is_admin=False,
            email_verified=True
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        
        # Create alumni profile
        alumni = Alumni(
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            matriculation_number=form.matriculation_number.data,
            faculty=form.faculty.data,
            department=form.department.data,
            graduation_year=form.graduation_year.data,
            degree=form.degree.data
        )
        db.session.add(alumni)
        db.session.commit()
        
        # TODO: Send verification email
        
        # flash('Registration successful! Please check your email to verify your account.', 'success')
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # TODO: Generate reset token and send email
            flash('If your email is registered, you will receive password reset instructions.', 'info')
        else:
            # Don't reveal if email exists or not for security
            flash('If your email is registered, you will receive password reset instructions.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # TODO: Validate token
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # TODO: Update password based on token
        flash('Your password has been reset successfully. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth.route('/verify-email/<token>')
def verify_email(token):
    # TODO: Implement email verification
    flash('Your email has been verified. You can now log in.', 'success')
    return redirect(url_for('auth.login'))
