from db import db
from datetime import datetime

class ForumTopic(db.Model):
    __tablename__ = 'forum_topics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    posts = db.relationship('ForumPost', backref='topic', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<ForumTopic {self.title}>'
    
    @property
    def post_count(self):
        return len(self.posts)
        
    @property
    def last_activity(self):
        if not self.posts:
            return self.created_at
        return max(post.created_at for post in self.posts)


class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    topic_id = db.Column(db.Integer, db.ForeignKey('forum_topics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<ForumPost {self.id} by User {self.user_id}>'
    
    @property
    def like_count(self):
        return len(self.likes)


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_post_user_like_uc'),)
    
    def __repr__(self):
        return f'<PostLike post_id={self.post_id} user_id={self.user_id}>'


class SupportGroup(db.Model):
    __tablename__ = 'support_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    meeting_frequency = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    memberships = db.relationship('GroupMembership', backref='group', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<SupportGroup {self.name}>'
    
    @property
    def member_count(self):
        return len(self.memberships)
        
    @property
    def next_meeting(self):
        # In a real app, would calculate based on meeting_frequency
        # For now, using a placeholder logic
        return datetime.utcnow()


class GroupMembership(db.Model):
    __tablename__ = 'group_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('support_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('group_id', 'user_id', name='_group_user_membership_uc'),)
    
    def __repr__(self):
        return f'<GroupMembership group_id={self.group_id} user_id={self.user_id}>'


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    organizer = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    registrations = db.relationship('EventRegistration', backref='event', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    @property
    def attendee_count(self):
        return len(self.registrations)


class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='_event_user_registration_uc'),)
    
    def __repr__(self):
        return f'<EventRegistration event_id={self.event_id} user_id={self.user_id}>'