from app import app
from models_data import db, User, Todo

with app.app_context():
    db.drop_all() #eliminer apres
    db.create_all()

    print("Database created")