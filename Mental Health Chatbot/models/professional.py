from extensions import db
from datetime import datetime

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(120), nullable=True)
    specialty = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    session_cost = db.Column(db.String(20), nullable=False)
    video_intro = db.Column(db.String(200), nullable=True)
    professional_type = db.Column(db.String(50), nullable=False)  # psychologist, psychiatrist, counselor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    education = db.relationship('ProfessionalEducation', backref='professional', lazy=True, cascade="all, delete-orphan")
    approaches = db.relationship('ProfessionalApproach', backref='professional', lazy=True, cascade="all, delete-orphan")
    insurance = db.relationship('ProfessionalInsurance', backref='professional', lazy=True, cascade="all, delete-orphan")
    languages = db.relationship('ProfessionalLanguage', backref='professional', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('ProfessionalReview', backref='professional', lazy=True, cascade="all, delete-orphan")
    appointments = db.relationship('Appointment', backref='professional', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Professional {self.name}>'
    
    @property
    def rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @property
    def review_count(self):
        return len(self.reviews)


class ProfessionalEducation(db.Model):
    __tablename__ = 'professional_education'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    education = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<ProfessionalEducation {self.education}>'


class ProfessionalApproach(db.Model):
    __tablename__ = 'professional_approaches'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    approach = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<ProfessionalApproach {self.approach}>'


class ProfessionalInsurance(db.Model):
    __tablename__ = 'professional_insurance'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    insurance = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<ProfessionalInsurance {self.insurance}>'


class ProfessionalLanguage(db.Model):
    __tablename__ = 'professional_languages'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<ProfessionalLanguage {self.language}>'


class ProfessionalReview(db.Model):
    __tablename__ = 'professional_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    helpful_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<ProfessionalReview id={self.id} rating={self.rating}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    session_type = db.Column(db.String(50), nullable=False)  # video, phone, in-person
    notes = db.Column(db.Text, nullable=True)
    confirmation_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, completed
    
    def __repr__(self):
        return f'<Appointment id={self.id} date={self.date} time={self.time}>'