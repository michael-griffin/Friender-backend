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


class Like(db.Model):
    """Table for user's likes"""
    __tablename__ = 'likes'
    user_liking = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    user_being_liked = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    @classmethod
    def add_like(cls, user_liking, user_being_liked):
        like = cls(user_liking=user_liking, user_being_liked=user_being_liked)
        db.session.add(like)

        return like


class DisLike(db.Model):
    """Table for user's likes"""
    __tablename__ = 'dislikes'
    user_disliking = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    user_being_disliked = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    @classmethod
    def add_dislike(cls, user_disliking, user_being_disliked):
        dislike = cls(user_disliking=user_disliking,
                      user_being_disliked=user_being_disliked)
        db.session.add(dislike)

        return dislike

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

    #all users the current user has liked, as well as all other users who like
    #the current user
    users_liked = db.relationship(
        "User",
        secondary="likes",
        primaryjoin=(Like.user_liking == username),
        secondaryjoin=(Like.user_being_liked == username),
        backref="liked_by",
    )


    @classmethod
    def signup(cls, username, password, hobbies, interests, location, radius=10):
        """Method to sign up a new user"""

        hashed_pwd = bcrypt.generate_password_hash(
            password).decode('UTF-8')

        new_user = User(username=username, password=hashed_pwd, hobbies=hobbies,
                        interests=interests, location=location, radius=radius)

        db.session.add(new_user)

        # jwt encode token based off
        jwt_token = jwt.encode(new_user.serialize(),
                               os.environ['SECRET_KEY'], algorithm='HS256')
        return jwt_token

    @classmethod
    def authenticate(cls, username, password):
        """Decode and confirm user password for user auth"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user:

            if bcrypt.check_password_hash(user.password, password):
                jwt_token = jwt.encode(
                    user.serialize(), os.environ['SECRET_KEY'], algorithm='HS256')
                return jwt_token
        else:
            return False

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "username": self.username,
            "hobbies": self.hobbies,
            "interests": self.interests,
            "location": self.location,
            "radius": self.radius
        }










# class Like(db.Model):
#     """Table for user's likes/dislikes"""
#     __tablename__ = 'likes'
#     username1 = db.Column(
#         db.String,
#         db.ForeignKey('users.username', ondelete="cascade"),
#         primary_key=True
#     )

#     username2 = db.Column(
#         db.String,
#         db.ForeignKey('users.username', ondelete="cascade"),
#         primary_key=True
#     )

#     user1_liked = db.Column(
#         db.Boolean,
#         nullable=True
#     )

#     user2_liked = db.Column(
#         db.Boolean,
#         nullable=True
#     )