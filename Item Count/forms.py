from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    shelfname = StringField("Shelfname", validators=[DataRequired(), Length(min=7, max=9)])
    submit = SubmitField("Submit")
