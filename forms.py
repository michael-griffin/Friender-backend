from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, Email, URL, Optional, NumberRange



class LoginForm(FlaskForm):
    """Form for logging in returning users"""

    username = StringField("Username", validators=[InputRequired(), Length(max=15)])

    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=5, max=50)])


class SignupForm(LoginForm):
    """Form for signing up new uers"""

    hobbies = StringField("Hobbies", validators=[InputRequired()])

    interests = StringField("Interests", validators=[InputRequired()])

    location = IntegerField("Location", validators=[NumberRange(min=10000, max=99999)])

    radius = IntegerField("Radius", validators=[Optional(), NumberRange(min=1, max=100)])
