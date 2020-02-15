from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

class DetailsForm(FlaskForm):
    choices = []
    c = 0
    for j in ['AM', 'PM']:
        for i in range(12):
            if i == 0:
                i = 12
            if i < 10:
                s = '0' + str(i)
            else:
                s = str(i)
            choices.append((c, s + ':00' + j))
            c += 1

    #email = StringField('Email', validators=[DataRequired(), Email()])
    #city = StringField('City', validators=[DataRequired()])
    #mail_time = SelectField('Mail Time', choices = choices, coerce=int, default=0)
    submit = SubmitField('Sign Up')
