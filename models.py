import os
from aws_utils import get_image_url

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


class Rating(db.Model):
    """Table for user's likes/dislikes"""
    __tablename__ = 'ratings'

    user_who_rated = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    user_being_rated = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete="cascade"),
        primary_key=True
    )

    is_liked = db.Column(
        db.Boolean,
        nullable=False
    )

    @classmethod
    def add_rating(cls, user_who_rated, user_being_rated, is_liked):
        rating = cls(user_who_rated=user_who_rated,
                     user_being_rated=user_being_rated, is_liked=is_liked)

        db.session.add(rating)

        return rating


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

    images = db.relationship("Image", backref="user")

    # all users the current user has liked, as well as all other users who like
    # the current user

    # users_liked = db.relationship(
    #     "User",
    #     secondary="ratings",
    #     primaryjoin=(Rating.user_who_rated == username),
    #     secondaryjoin=(Rating.user_being_rated == username),
    #     backref="rated_by",
    # )

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

    # def get_users_liked_v2(self):
    #     users = db.session.query(User, Rating
    #                             ).join(Rating, User.username == Rating.user_being_rated
    #                             ).filter(Rating.is_liked)

    #     return users

    def get_matches(self):
        ratings = Rating.query.all()

        users_liked = []
        users_liking_you = []
        for rating in ratings:
            if rating.user_who_rated == self.username and rating.is_liked:
                users_liked.append(rating.user_being_rated)

            if rating.user_being_rated == self.username and rating.is_liked:
                users_liking_you.append(rating.user_who_rated)

        matches = list(set(users_liked) & set(users_liking_you))
        matching_users = User.query.filter(User.username.in_(matches))

        return matching_users

    def get_unrated(self):
        ratings = Rating.query.all()
        rated_users = [self.username]

        for rating in ratings:
            if rating.user_who_rated == self.username:
                rated_users.append(rating.user_being_rated)

        unrated_users = User.query.filter(~ User.username.in_(rated_users))
        return unrated_users

    # TODO: make location check smarter

    def get_eligible(self):
        unrated_users = self.get_unrated()

        min_location = self.location - self.radius
        max_location = self.location + self.radius

        eligible_users = unrated_users.filter(
            User.location <= max_location,
            User.location >= min_location
        )

        return eligible_users

    def serialize(self):
        """Serialize to dictionary."""

        image_urls = [i.serialize() for i in self.images]

        return {
            "username": self.username,
            "hobbies": self.hobbies,
            "interests": self.interests,
            "location": self.location,
            "radius": self.radius,
            "image_urls" : image_urls
        }



class Image(db.Model):
    """Model for images users have uploaded"""

    __tablename__ = "images"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(15),
        db.ForeignKey('users.username', ondelete="cascade"),
        nullable=False
    )

    img_name = db.Column(
        db.String(),
        nullable=False
    )

    @classmethod
    def add_image(cls, username, img_name):
        image = cls(username=username, img_name=img_name)
        db.session.add(image)

        return image

    def serialize(self):
        """calls s3 function to return a pre-signed url, expires in 1 hour."""
        image_url = get_image_url(self.img_name)
        return image_url
