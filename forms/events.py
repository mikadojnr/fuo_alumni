from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateTimeField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length, URL

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired(), Length(min=20)])
    date = DateTimeField('Start Date and Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    end_date = DateTimeField('End Date and Time', validators=[Optional()], format='%Y-%m-%d %H:%M')
    location = StringField('Location', validators=[Optional(), Length(max=255)])
    is_virtual = BooleanField('Virtual Event')
    virtual_link = StringField('Virtual Meeting Link', validators=[Optional(), URL(), Length(max=255)])
    image = FileField('Event Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    
    submit = SubmitField('Save Event')

class EventRegistrationForm(FlaskForm):
    attendance_type = SelectField('How will you attend?', choices=[
        ('in_person', 'In Person'),
        ('virtual', 'Virtual')
    ])
    
    submit = SubmitField('Register for Event')
