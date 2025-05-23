from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Contribution, Project, Alumni
from forms.contributions import ContributionForm
from extensions import db
from datetime import datetime

contributions = Blueprint('contributions', __name__, url_prefix='/contributions')

@contributions.route('/')
def index():
    # Get active projects
    active_projects = Project.query.filter_by(is_active=True).all()
    
    # Get completed projects
    completed_projects = Project.query.filter_by(is_active=False).all()

    # Compute total amount (just an example - adjust as needed)
    total_amount = sum(project.current_amount for project in active_projects + completed_projects)
    
    # Compute total contributions
    total_contributions = len(active_projects) + len(completed_projects)  # Example metric

    return render_template('contributions/index.html',
                           active_projects=active_projects,
                           completed_projects=completed_projects,
                           total_amount=total_amount,
                           total_contributions=total_contributions)


@contributions.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Get contributions for this project (non-anonymous only)
    contributions = Contribution.query.filter_by(project_id=project.id, is_anonymous=False).order_by(Contribution.created_at.desc()).all()
    
    # Contribution form
    form = ContributionForm()
    
    return render_template('contributions/project_detail.html',
                          project=project,
                          contributions=contributions,
                          form=form)

"""
@contributions.route('/project/<int:project_id>/contribute', methods=['POST'])
@login_required
def contribute(project_id):
    if current_user.is_admin:
        flash('Admins cannot make contributions.', 'warning')
        return redirect(url_for('contributions.project_detail', project_id=project_id))
    
    project = Project.query.get_or_404(project_id)
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()
    
    # Check if project is active
    if not project.is_active:
        flash('This project is no longer accepting contributions.', 'warning')
        return redirect(url_for('contributions.project_detail', project_id=project_id))
    
    form = ContributionForm()
    if form.validate_on_submit():
        # Create contribution
        contribution = Contribution(
            alumni_id=alumni.id,
            project_id=project.id,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            is_anonymous=form.is_anonymous.data,
            dedication=form.dedication.data
        )
        
        db.session.add(contribution)
        db.session.commit()
        
        flash('Thank you for your contribution!', 'success')
        return redirect(url_for('contributions.project_detail', project_id=project_id))
    
    # If form validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    
    return redirect(url_for('contributions.project_detail', project_id=project_id))
"""

import uuid
from flask import session
# import paypalrestsdk # Only needed for real PayPal integration

@contributions.route('/project/<int:project_id>/contribute', methods=['POST'])
@login_required
def contribute(project_id):
    if current_user.is_admin:
        flash('Admins cannot make contributions.', 'warning')
        return redirect(url_for('contributions.project_detail', project_id=project_id))

    project = Project.query.get_or_404(project_id)
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()

    if not project.is_active:
        flash('This project is no longer accepting contributions.', 'warning')
        return redirect(url_for('contributions.project_detail', project_id=project_id))

    form = ContributionForm()
    if form.validate_on_submit():
        if form.payment_method.data == 'paypal':
            # Step 1: Create a temporary contribution object (not committed to DB yet)
            contribution_data = {
                'alumni_id': alumni.id,
                'project_id': project.id,
                'amount': form.amount.data,
                'payment_method': 'paypal',
                'is_anonymous': form.is_anonymous.data,
                'dedication': form.dedication.data,
            }

            # Step 2: Simulate PayPal redirect
            session['pending_contribution'] = contribution_data
            session['paypal_payment_id'] = str(uuid.uuid4())  # Simulate a PayPal payment ID

            # Redirect to a simulated PayPal approval route
            return redirect(url_for('contributions.simulate_paypal_approval'))

        # Other payment methods
        contribution = Contribution(
            alumni_id=alumni.id,
            project_id=project.id,
            amount=form.amount.data,
            payment_method=form.payment_method.data,
            is_anonymous=form.is_anonymous.data,
            dedication=form.dedication.data
        )
        db.session.add(contribution)
        db.session.commit()
        flash('Thank you for your contribution!', 'success')
        return redirect(url_for('contributions.project_detail', project_id=project_id))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('contributions.project_detail', project_id=project_id))

@contributions.route('/paypal/approve')
@login_required
def simulate_paypal_approval():
    # Simulate user approving the payment on PayPal
    return redirect(url_for('contributions.paypal_execute'))


@contributions.route('/paypal/execute')
@login_required
def paypal_execute():
    contribution_data = session.pop('pending_contribution', None)
    paypal_payment_id = session.pop('paypal_payment_id', None)

    if not contribution_data or not paypal_payment_id:
        flash('Invalid PayPal session.', 'danger')
        return redirect(url_for('main.index'))

    # Simulate a successful PayPal payment execution
    # In real app: verify payment with PayPal API using `paypal_payment_id`

    contribution = Contribution(**contribution_data)
    db.session.add(contribution)
    db.session.commit()

    flash('Thank you for your PayPal contribution!', 'success')
    return redirect(url_for('contributions.project_detail', project_id=contribution.project_id))



@contributions.route('/history')
@login_required
def history():
    if current_user.is_admin:
        return redirect(url_for('admin.contributions'))
    
    alumni = Alumni.query.filter_by(user_id=current_user.id).first()
    contributions = Contribution.query.filter_by(alumni_id=alumni.id).order_by(Contribution.created_at.desc()).all()
    
    return render_template('contributions/history.html', contributions=contributions, alumni=alumni)

@contributions.route('/receipt/<int:contribution_id>')
@login_required
def receipt(contribution_id):
    # Check if admin or contribution owner
    contribution = Contribution.query.get_or_404(contribution_id)
    
    if not current_user.is_admin:
        alumni = Alumni.query.filter_by(user_id=current_user.id).first()
        if contribution.alumni_id != alumni.id:
            flash('Access denied.', 'danger')
            return redirect(url_for('contributions.history'))
    
    return render_template('contributions/receipt.html', contribution=contribution)
