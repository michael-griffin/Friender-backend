#Coming soon
import os

from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///DATABASE_NAME')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



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



#Select all users who current user has matched with.
@app.get('/users/<int:id>/matches')
def get_matched_users():


#Like/Dislike a user (POST)
@app.post('/likes')
def toggle_like():
    likeStatus = request.json('like')
    fromUser = request.json('fromUser')
    toUser = request.json('toUser')

    newLike = Like(likeStatus = likeStatus,
                    fromUser = fromUser,
                    toUser = toUser)

    db.session.add(newLike)
    db.session.commit(newLike)

    confirm_msg = {"message": "dislike successful"}
    return (jsonify(confirm_msg), 201)



#Add/log message between two users
@app.post('/messages')
def log_message():
    message = request.json('message')
    fromUser = request.json('fromUser')
    toUser = request.json('toUser')

    newMessage = Message(message = message,
                         fromUser = fromUser,
                         toUser = toUser)

    db.session.add(newMessage)
    db.session.commit()

    return (jsonify(newMessage.serialize()), 201)