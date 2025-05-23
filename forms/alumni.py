from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange
from datetime import datetime

class ProfileForm(FlaskForm):
    # Personal Info
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[Optional(), Length(max=50)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    profile_photo = FileField('Profile Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    bio = TextAreaField('Bio/About Me', validators=[Optional(), Length(max=500)])
    
    # Academic Info
    matriculation_number = StringField('Matriculation Number', validators=[DataRequired(), Length(min=5, max=20)])
    faculty = SelectField('Faculty', validators=[DataRequired()], choices=[
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
    
    # Professional Info
    job_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    organization = StringField('Organization/Company', validators=[Optional(), Length(max=100)])
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    linkedin_url = StringField('LinkedIn Profile URL', validators=[Optional(), URL()])
    
    # Privacy Settings
    show_email = BooleanField('Show Email to Other Alumni')
    show_phone = BooleanField('Show Phone Number to Other Alumni')
    show_job = BooleanField('Show Job Information to Other Alumni')
    
    submit = SubmitField('Update Profile')
