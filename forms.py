from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    """Form for logging in returning users"""

    username = StringField("Username", validators=[
                           InputRequired(), Length(max=15)])

    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=5, max=50)])


class SignupForm(LoginForm):
    """Form for signing up new uers"""

    hobbies = StringField("Hobbies", validators=[InputRequired()])

    interests = StringField("Interests", validators=[InputRequired()])

    location = IntegerField("Location", validators=[
                            NumberRange(min=10000, max=99999)])

    radius = IntegerField("Radius", validators=[
                          Optional(), NumberRange(min=1, max=100)])


class RatingForm(FlaskForm):
    """form for one user to rate another"""

    user_who_rated = StringField('User Who Rated', validators=[
                                 InputRequired(), Length(max=15)])

    user_being_rated = StringField('User Being Rated', validators=[
        InputRequired(), Length(max=15)])

    is_liked = BooleanField("Is Liked", validators=[InputRequired()])



class MessageForm(FlaskForm):
    """form for one user to rate another"""

    sender = StringField('Sender', validators=[
                                 InputRequired(), Length(max=15)])

    receiver = StringField('Receiver', validators=[
        InputRequired(), Length(max=15)])

    message = StringField("Is Liked", validators=[InputRequired()])