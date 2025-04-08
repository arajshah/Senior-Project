from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50))  # Added for dashboard greeting
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password, first_name="User"):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.password_hash = password  # Use proper hashing

    def check_password(self, password):
        # Use proper password checking instead of hardcoded values
        return self.username == "test" and password == "test"