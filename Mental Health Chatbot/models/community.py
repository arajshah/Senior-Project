from db import db
from datetime import datetime

class Forum(db.Model):
    """Forum model for different discussion topics"""
    __tablename__ = 'forums'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship with posts
    posts = db.relationship('ForumPost', backref='forum', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Forum {self.title}>'

class ForumPost(db.Model):
    """Post model for forum discussions"""
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign keys
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship with replies
    replies = db.relationship('PostReply', backref='post', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<ForumPost {self.title}>'

class PostReply(db.Model):
    """Reply model for forum posts"""
    __tablename__ = 'post_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign keys
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<PostReply {self.id}>'

class SupportGroup(db.Model):
    """Support Group model"""
    __tablename__ = 'support_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    meeting_schedule = db.Column(db.String(100), nullable=False)
    facilitator = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, default=20)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship with members (many-to-many)
    members = db.relationship('User', secondary='group_members', backref=db.backref('groups', lazy='dynamic'))
    
    def __repr__(self):
        return f'<SupportGroup {self.name}>'

# Association table for support group members
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('support_groups.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.now)
)

class Event(db.Model):
    """Virtual Event model"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    host = db.Column(db.String(100), nullable=False)
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship with attendees (many-to-many)
    attendees = db.relationship('User', secondary='event_attendees', backref=db.backref('events', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Event {self.title}>'

# Association table for event attendees
event_attendees = db.Table('event_attendees',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True),
    db.Column('registered_at', db.DateTime, default=datetime.now)
)