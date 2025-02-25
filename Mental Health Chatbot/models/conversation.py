from db import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    assistant_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to easily access the user object
    user = db.relationship("User", backref="conversations")

    def __init__(self, user_id, user_message, assistant_response):
        self.user_id = user_id
        self.user_message = user_message
        self.assistant_response = assistant_response
