from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime
from sqlalchemy import CheckConstraint, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class Todo(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    due_time = db.Column(db.Time)
    status = db.Column(db.String(12), default = 'PENDING', nullable=False)

    #created_at = db.Column(db.DateTime, default=datetime.utcnow)


    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'DONE')",
            name="check_status_valid"
        ),
    )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    todos = db.relationship("Todo", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    



    
