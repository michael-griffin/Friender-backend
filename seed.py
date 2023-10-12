from app import db
from models import User, Rating, Image  # , Message, Like

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

user4 = User.signup(username='test_user4',
                    password='password',
                    hobbies='not much',
                    interests='testing',
                    location=10002,
                    radius=2)

user5 = User.signup(username='test_user5',
                    password='password',
                    hobbies='not much',
                    interests='testing',
                    location=10002,
                    radius=2)

user6 = User.signup(username='test_user6',
                    password='password',
                    hobbies='living away from people',
                    interests='testing',
                    location=60002,
                    radius=2)


db.session.commit()

rating1 = Rating.add_rating('test_user1', 'test_user2', True)
rating2 = Rating.add_rating('test_user2', 'test_user1', True)
rating3 = Rating.add_rating('test_user1', 'test_user3', True)

image1 = Image.add_image('test_user1', 'Dawid-Planeta-fox.jpg')
image2 = Image.add_image('test_user1', 'Dawid-Planeta-whale.jpg')
image3 = Image.add_image('test_user3', 'mem-game2.png')

db.session.commit()
