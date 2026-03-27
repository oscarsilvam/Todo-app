from app import create_app
from models_data import db

app = create_app()

with app.app_context():
    db.drop_all() #eliminer apres
    db.create_all()

    print("Database created")