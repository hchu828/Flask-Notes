from models import db, User, Note
from app import app


db.drop_all()
db.create_all()

user1 = User(
    username="n8snyder",
    password="^bhfu9tbruBU(WIFGH(",
    email="fake@mail.com",
    first_name="Nate",
    last_name="Snyder",
)

user2 = User(
    username="hchu828",
    password="GT&8ghEW&*FHE&*fgasfg",
    email="fake2@mail.com",
    first_name="Hector",
    last_name="Chu",
)

test_user = User.register(
    "test_user", "1234", "test@test.com", "test_first", "test_last"
)

db.session.add_all([user1, user2, test_user])
db.session.commit()

note = Note(title="title", content="some text", owner="test_user")
db.session.add(note)
db.session.commit()
