from app import db
from models import User, Rating, Image, Message  # , Like

db.drop_all()
db.create_all()


user1 = User.signup(username='test_user1',
                    password='password',
                    hobbies='skateboarding, cooking',
                    interests='coding at rithm',
                    location=10000,
                    radius=50)


user2 = User.signup(username='test_user2',
                    password='password',
                    hobbies='taking vitamins',
                    interests='testing',
                    location=10002,
                    radius=2)

user3 = User.signup(username='test_user3',
                    password='password',
                    hobbies='base jumping',
                    interests='testing',
                    location=10003,
                    radius=2)

user4 = User.signup(username='test_user4',
                    password='password',
                    hobbies='mountaineering',
                    interests='testing',
                    location=10004,
                    radius=2)

user5 = User.signup(username='test_user5',
                    password='password',
                    hobbies='origami',
                    interests='testing',
                    location=10005,
                    radius=50)

user6 = User.signup(username='test_user6',
                    password='password',
                    hobbies='calligraphy',
                    interests='testing',
                    location=10006,
                    radius=50)

user7 = User.signup(username='test_user7',
                    password='password',
                    hobbies='juggling',
                    interests='testing',
                    location=10007,
                    radius=50)

user8 = User.signup(username='test_user8',
                    password='password',
                    hobbies='puppetry, soap making',
                    interests='testing',
                    location=10008,
                    radius=50)

user9 = User.signup(username='test_user9',
                    password='password',
                    hobbies='woodworking',
                    interests='testing',
                    location=10012,
                    radius=50)

user10 = User.signup(username='test_user10',
                    password='password',
                    hobbies='living away from people',
                    interests='being alone',
                    location=60002,
                    radius=2)


db.session.commit()
image1 = Image.add_image('test_user1', 'Dawid-Planeta-fox.jpg')
image2 = Image.add_image('test_user1', 'Dawid-Planeta-whale.jpg')
image3 = Image.add_image('test_user3', 'mem-game2.png')


rating1 = Rating.add_rating('test_user1', 'test_user2', True)
rating2 = Rating.add_rating('test_user2', 'test_user1', True)
rating3 = Rating.add_rating('test_user3', 'test_user1', True)
rating4 = Rating.add_rating('test_user4', 'test_user1', True)
rating5 = Rating.add_rating('test_user5', 'test_user1', True)
rating6 = Rating.add_rating('test_user6', 'test_user1', True)
rating7 = Rating.add_rating('test_user7', 'test_user1', True)
rating8 = Rating.add_rating('test_user8', 'test_user1', True)
rating9 = Rating.add_rating('test_user9', 'test_user1', True)
rating10 = Rating.add_rating('test_user10', 'test_user1', True)



message1 = Message.add_message('test_user1', 'test_user2', 'first post')
message2 = Message.add_message('test_user2', 'test_user1', 'second')
message3 = Message.add_message(
    'test_user1', 'test_user2', 'how are you doing today?')


db.session.commit()
