#Coming soon
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, redirect, g
import jwt

from models import db, connect_db, User
from forms import SignupForm, LoginForm
from sqlalchemy.exc import IntegrityError


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
    token = request.json.get('token')

    if token:
        payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])

        if payload.user:
            g.user = User.query.get(payload.user.username)


##signup route -> assuming successful signup, returns token
# (used to get user on front end). Possible error for incorrect signup
@app.post('/signup')
def signup():

    #JSONValidateForm(form_data=request.json, meta={'csrf': False})

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
            return (jsonify({'token' : token}), 201)
        except IntegrityError:
            return jsonify({'error': 'username already taken'})

    return jsonify({'error': 'invalid form data'})



##login -> returns token, error if invalid credentials
@app.post('/login')
def login():
    form = LoginForm(form_data=request.json, meta={'csrf': False})
    if form.validate_on_submit():
        token = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        if token:
            return jsonify({'token': token})

    return jsonify({'error': "Username or password incorrect"})



#GET all users
@app.get('/users')
def get_all_users():
    users = User.query.all()

    serialized = [user.serialize() for user in users]
    return jsonify(users = serialized)

#GET user detail
@app.get('/users/<int:id>')
def get_user_details():
    user = User.query.get_or_404(id)

    serialized = user.serialize()
    return jsonify(user = serialized)


#Find eligible users for liking/disliking. Filters all users by radius,
#then, filter again to remove any they have liked/disliked previously.
#return a list of remaining
@app.get('/users/<int:id>/nearme')
def get_eligible_users():
    return False


#Select all users who current user has matched with.
@app.get('/users/<int:id>/matches')
def get_matched_users():
    return False




# #Like/Dislike a user (POST)
# @app.post('/likes')
# def toggle_like():
#     likeStatus = request.json('like')
#     fromUser = request.json('fromUser')
#     toUser = request.json('toUser')

#     newLike = Like(likeStatus = likeStatus,
#                     fromUser = fromUser,
#                     toUser = toUser)

#     db.session.add(newLike)
#     db.session.commit(newLike)

#     confirm_msg = {"message": "dislike successful"}
#     return (jsonify(confirm_msg), 201)



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