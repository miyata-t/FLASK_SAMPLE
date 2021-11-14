from models.database_manager import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(30), nullable=True)
