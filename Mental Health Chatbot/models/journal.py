from db import db
from datetime import datetime

class Journal(db.Model):
    __tablename__ = 'journals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # Added title field
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, title, content):
        self.user_id = user_id
        self.title = title
        self.content = content