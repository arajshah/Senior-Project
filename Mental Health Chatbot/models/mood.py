from db import db
from datetime import datetime

class Mood(db.Model):
    __tablename__ = 'moods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1-10 scale
    note = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, score, note=None):
        self.user_id = user_id
        self.score = score
        self.note = note