from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, BooleanField, DecimalField, SelectField, PasswordField, FileField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, NumberRange, ValidationError
from flask_wtf.file import FileAllowed

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeLocalField('Event Date', validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date', validators=[Optional()])
    is_virtual = BooleanField('Virtual Event')
    location = StringField('Location', validators=[Length(max=200)])
    virtual_link = StringField('Virtual Meeting Link', validators=[Length(max=255)])
    image = FileField('Event Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Create Event')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    goal_amount = DecimalField('Goal Amount (₦)', validators=[DataRequired(), NumberRange(min=1000)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    is_active = BooleanField('Is Active')
    image = FileField('Project Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Project')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    is_active = BooleanField('Active')
    is_admin = BooleanField('Admin')
    
    # Admin fields (only used if is_admin is True)
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    role = StringField('Role', validators=[Optional(), Length(max=50)])

class ContributionForm(FlaskForm):
    alumni_id = SelectField('Alumni', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Amount (₦)', validators=[DataRequired(), NumberRange(min=100)])
    payment_method = SelectField('Payment Method', choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal')
    ], validators=[DataRequired()])
    transaction_id = StringField('Transaction ID', validators=[DataRequired(), Length(max=50)])
    is_anonymous = BooleanField('Anonymous Contribution')
    dedication = TextAreaField('Dedication', validators=[Optional(), Length(max=255)])

class SettingsForm(FlaskForm):
    site_name = StringField('Site Name', validators=[DataRequired(), Length(max=100)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    footer_text = TextAreaField('Footer Text', validators=[Optional()])
    
    # Social media
    facebook_url = StringField('Facebook URL', validators=[Optional(), Length(max=255)])
    twitter_url = StringField('Twitter URL', validators=[Optional(), Length(max=255)])
    instagram_url = StringField('Instagram URL', validators=[Optional(), Length(max=255)])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), Length(max=255)])
    
    # Email settings
    smtp_server = StringField('SMTP Server', validators=[Optional(), Length(max=100)])
    smtp_port = IntegerField('SMTP Port', validators=[Optional()])
    smtp_username = StringField('SMTP Username', validators=[Optional(), Length(max=100)])
    smtp_password = PasswordField('SMTP Password', validators=[Optional()])
    
    # Features
    enable_registration = BooleanField('Enable Registration')
    enable_donations = BooleanField('Enable Donations')
    enable_events = BooleanField('Enable Events')
    require_email_verification = BooleanField('Require Email Verification')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    role = StringField('Role', validators=[Optional(), Length(max=50)])
    
    # Password change fields
    current_password = PasswordField('Current Password', validators=[Optional()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        Optional(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_password(self, field):
        if field.data and not self.current_password.data:
            raise ValidationError('Current password is required to set a new password')


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Announcement')