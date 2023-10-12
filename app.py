# Coming soon
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, g
import jwt
import tempfile

from models import db, connect_db, User, Rating, Image
from forms import SignupForm, LoginForm, RatingForm
from sqlalchemy.exc import IntegrityError

from aws_utils import get_image_url, upload_image

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///friender')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)

################# Auth Routes ###################


@app.before_request
def check_for_token():
    """Check for token before each request"""

    token = request.headers.get('token')

    # token = request.json.get('token')

    if token:
        payload = jwt.decode(
            token, os.environ['SECRET_KEY'], algorithms=['HS256'])

        print('!!!!!!!!!!!!!! \n\n\n token is:', token)
        if payload['username']:
            g.user = User.query.get(payload['username'])
        else:
            g.user = None
    else:
        print('!!!!!!!!!!!!!! \n\n\n token falsy, token is:', token)
        g.user = None


@app.after_request
def after_request(response):
    header = response.headers
    header.add("Access-Control-Allow-Origin", "*")
    header.add('Access-Control-Allow-Headers', "*")
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.post('/signup')
def signup():
    """Route to signup user, returns token or error message"""

    form = SignupForm(form_data=request.json, meta={'csrf': False})
    if form.validate_on_submit():
        try:
            token = User.signup(username=form.username.data,
                                password=form.password.data,
                                hobbies=form.hobbies.data,
                                interests=form.interests.data,
                                location=form.location.data,
                                radius=form.radius.data)

            db.session.commit()
            return (jsonify({'token': token}), 201)
        except IntegrityError:
            return jsonify({'error': 'username already taken'})

    return jsonify({'error': 'invalid form data'})


@app.post('/login')
def login():
    """Route to login user, returns token or error message"""

    # print(f"request json is: {request}")
    # if request.json is None:
    #     return ({'error': 'no json sent'})

    form = LoginForm(form_data=request.json, meta={'csrf': False})
    if form.validate_on_submit():
        token = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        if token:
            return jsonify({'token': token})

    return jsonify({'error': "Username or password incorrect"})


####### User Routes ########

# GET all users
@app.get('/users')
def get_all_users():

    if not g.user:
        return (jsonify({'error': 'You are not authorized to access this'}), 404)

    users = User.query.all()

    serialized = [user.serialize() for user in users]
    return jsonify(users=serialized)


# GET user detail
@app.get('/users/<string:username>')
def get_user_details(username):
    user = User.query.get_or_404(username)

    serialized = user.serialize()
    return jsonify(user=serialized)


# Find eligible users for liking/disliking. Filters all users by radius,
# then, filter again to remove any they have liked/disliked previously.
# return a list of remaining
@app.get('/users/<string:username>/nearme')
def get_eligible_users(username):
    """Route to get unrated users within logged in user's search radius"""
    user = User.query.get_or_404(username)

    eligible = user.get_eligible().all()

    eligible = [u.serialize() for u in eligible]

    return jsonify(eligible=eligible)


# Select all users who current user has matched with.
@app.get('/users/<string:username>/matches')
def get_matched_users(username):
    """"""

    user = User.query.get_or_404(username)

    matches = user.get_matches().all()
    matches = [u.serialize() for u in matches]

    return jsonify(matches=matches)


# Fields they can update are?
@app.patch('/users/<string:username>')
def update_user(username):

    if not g.user or g.user.username != username:
        return jsonify({'error': 'unauthorized'})

    # get_or_404 as alternative?
    user = User.query.get(username)

    user.hobbies = request.json.get('hobbies', user.hobbies)
    user.interests = request.json.get('interests', user.interests)
    user.location = request.json.get('location', user.location)
    user.radius = request.json.get('radius', user.radius)

    db.session.commit()

    return jsonify(user.serialize())


@app.delete('/users/<string:username>')
def delete_user(username):

    if not g.user or g.user.username != username:
        return jsonify({'error': 'unauthorized'})

    User.query.filter(User.username == username).delete()
    db.session.commit()

    return jsonify({"deleted": username})


# Like/Dislike a user (POST)
@app.post('/rating')
def rate_user():
    """Route for one user to like another"""

    form = RatingForm(form_data=request.json, meta={'csrf': False})

    if form.validate_on_submit():
        try:

            Rating.add_rating(user_who_rated=form.user_who_rated.data,
                              user_being_rated=form.user_being_rated.data,
                              is_liked=form.is_liked.data)

            db.session.commit()

            return jsonify({'message': "rated user successfully"}, 201)

        except IntegrityError:
            return jsonify({'error': "Already rated user."})

    return jsonify({'error': "invalid json data"})


@app.post('/users/<string:username>/image')
def add_image(username):
    """Route for uploading an image for user"""
    image = request.files['image']

    with tempfile.TemporaryDirectory() as temp:
        image.save(os.path.join(temp, image.filename))
        upload_image(os.path.join(temp, image.filename), image.filename)

    Image.add_image(username, image.filename)
    db.session.commit()

    return jsonify({'message': 'Image added successfully.'}), 201


# #Add/log message between two users
# @app.post('/messages')
# def log_message():
#     message = request.json('message')
#     fromUser = request.json('fromUser')
#     toUser = request.json('toUser')

#     newMessage = Message(message = message,
#                          fromUser = fromUser,
#                          toUser = toUser)

#     db.session.add(newMessage)
#     db.session.commit()

#     return (jsonify(newMessage.serialize()), 201)
