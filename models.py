import os

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for User in Friender"""

    __tablename__ = "users"

    username = db.Column(
        db.String(15),
        primary_key=True
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    hobbies = db.Column(
        db.String(),
        nullable=False
    )

    interests = db.Column(
        db.String(),
        nullable=False
    )

    location = db.Column(
        db.Integer,
        nullable=False
    )

    radius = db.Column(
        db.Integer,
        nullable=False
    )

    @classmethod
    def signup(cls, username, password, hobbies, interests, location, radius=10):
        """Method to sign up a new user"""

        hashed_pwd = bcrypt.generate_password_hash(
            password).decode('UTF-8')

        new_user = User(username=username, password=hashed_pwd, hobbies=hobbies,
                        interests=interests, location=location, radius=radius)

        db.session.add(new_user)

        #jwt encode token based off
        jwt_token = jwt.encode(new_user.serialize(), os.environ['SECRET_KEY'], algorithm='HS256')
        return jwt_token

    @classmethod
    def authenticate(cls, username, password):
        """Decode and confirm user password for user auth"""

        user = cls.query.filter_by(username=username).one_or_none()

        unhashed_pwd = bcrypt.check_password_hash(password)

        if user.password == unhashed_pwd:
            jwt_token = jwt.encode(user.serialize(), os.environ['SECRET_KEY'], algorithm='HS256')
            return jwt_token
        else:
            return False

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "username": self.username,
            "hobbies" : self.hobbies,
            "interests" : self.interests,
            "location" : self.location,
            "radius" : self.radius
        }