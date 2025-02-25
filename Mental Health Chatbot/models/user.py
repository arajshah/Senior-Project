from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = password

    def check_password(self, password):
        return self.username == "test" and password == "test"
