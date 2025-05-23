from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class ContributionForm(FlaskForm):
    amount = DecimalField('Contribution Amount (₦)', validators=[
        DataRequired(),
        NumberRange(min=100, message='Minimum contribution amount is ₦100')
    ])
    payment_method = SelectField('Payment Method', validators=[DataRequired()], choices=[
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card')
    ])
    is_anonymous = BooleanField('Make this contribution anonymous')
    dedication = TextAreaField('Dedication or Message (Optional)', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Contribute')
