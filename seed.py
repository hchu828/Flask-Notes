from models import db, User
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

db.session.add_all([user1, user2])
db.session.commit()
