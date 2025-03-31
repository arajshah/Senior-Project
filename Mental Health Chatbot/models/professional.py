from db import db
from datetime import datetime

class Professional(db.Model):
    """Professional model for mental health professionals"""
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(50), nullable=False) # psychologist, psychiatrist, counselor
    credentials = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    specialties = db.Column(db.Text, nullable=False)
    years_experience = db.Column(db.Integer, nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    virtual_sessions = db.Column(db.Boolean, default=True)
    in_person_sessions = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(255), nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship with appointments
    appointments = db.relationship('Appointment', backref='professional', lazy=True)
    
    def __repr__(self):
        return f'<Professional {self.name} ({self.profession})>'

class Appointment(db.Model):
    """Appointment model for scheduling sessions with professionals"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60, nullable=False)
    status = db.Column(db.String(20), default='scheduled', nullable=False) # scheduled, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    meeting_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign keys
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Appointment {self.id}>'

class AvailabilitySlot(db.Model):
    """Availability slots for professionals"""
    __tablename__ = 'availability_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False) # 0-6 for Monday-Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Foreign key
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    
    def __repr__(self):
        return f'<AvailabilitySlot {self.day_of_week}: {self.start_time}-{self.end_time}>'