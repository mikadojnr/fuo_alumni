from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    
    # Academic Info
    matriculation_number = StringField('Matriculation Number', validators=[DataRequired(), Length(min=5, max=20)])
    faculty = SelectField('Faculty', validators=[DataRequired()], choices=[
        ('', 'Select Faculty'),
        ('Engineering', 'Engineering'),
        ('Science', 'Science'),
        ('Arts', 'Arts'),
        ('Social Sciences', 'Social Sciences'),
        ('Management Sciences', 'Management Sciences'),
        ('Education', 'Education'),
        ('Law', 'Law'),
        ('Medicine', 'Medicine')
    ])
    department = StringField('Department', validators=[DataRequired(), Length(min=2, max=100)])
    graduation_year = IntegerField('Graduation Year', validators=[
        DataRequired(),
        NumberRange(min=2000, max=datetime.now().year, message='Please enter a valid graduation year')
    ])
    degree = SelectField('Degree', validators=[DataRequired()], choices=[
        ('', 'Select Degree'),
        ('B.Sc.', 'Bachelor of Science (B.Sc.)'),
        ('B.A.', 'Bachelor of Arts (B.A.)'),
        ('B.Eng.', 'Bachelor of Engineering (B.Eng.)'),
        ('LL.B.', 'Bachelor of Laws (LL.B.)'),
        ('B.Ed.', 'Bachelor of Education (B.Ed.)'),
        ('M.Sc.', 'Master of Science (M.Sc.)'),
        ('M.A.', 'Master of Arts (M.A.)'),
        ('M.Eng.', 'Master of Engineering (M.Eng.)'),
        ('LL.M.', 'Master of Laws (LL.M.)'),
        ('M.Ed.', 'Master of Education (M.Ed.)'),
        ('Ph.D.', 'Doctor of Philosophy (Ph.D.)')
    ])
    
    # Password
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    # Agreement
    agree_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')
