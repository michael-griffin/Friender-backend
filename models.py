from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


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

        hashed_pwd = Bcrypt.generate_password_hash(
            password).decode('UTF-8')

        new_user = User(username=username, password=hashed_pwd, hobbies=hobbies,
                        interests=interests, location=location, radius=radius)

        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """Decode and confirm user password for user auth"""

        u = cls.query.filter_by(username=username).one_or_none()

        unhashed_pwd = Bcrypt.check_password_hash(password)

        if u.password == unhashed_pwd:
            return u
        else:
            return False
