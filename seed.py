from app import db
from models import User #, Message, Like

db.drop_all()
db.create_all()


user1 = User.signup(username='test_user1',
                    password='password',
                    hobbies='not much',
                    interests='testing',
                    location=10000,
                    radius=2)
user2 = User.signup(username='test_user2',
                    password='password',
                    hobbies='not much',
                    interests='testing',
                    location=10001,
                    radius=2)
user3 = User.signup(username='test_user3',
                    password='password',
                    hobbies='not much',
                    interests='testing',
                    location=10003,
                    radius=2)


# #Still need to add likes
# like1 = Like.add_like('test_user1', 'test_user2', True)
# like1 = Like.add_like('test_user1', 'test_user2', True)

db.session.commit()
