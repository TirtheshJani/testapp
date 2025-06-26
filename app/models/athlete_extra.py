from datetime import datetime
from app import db
from app.models.base import BaseModel

class Athlete(BaseModel):
    __tablename__ = 'athletes'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False, index=True)
    last_name = db.Column(db.String(100), nullable=False, index=True)
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    position = db.Column(db.String(50))
    sport_type = db.Column(db.String(50))
    team_history = db.Column(db.JSON)

    stats = db.relationship('AthleteStat', back_populates='athlete', cascade='all, delete-orphan')
    media = db.relationship('AthleteMedia', back_populates='athlete', cascade='all, delete-orphan')
    achievements = db.relationship('AthleteAchievement', back_populates='athlete', cascade='all, delete-orphan')

    __table_args__ = (
        db.Index('idx_athletes_name', 'last_name', 'first_name'),
    )

    def __repr__(self):
        return f'<Athlete {self.first_name} {self.last_name}>'

class AthleteStat(BaseModel):
    __tablename__ = 'athlete_stats'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id', ondelete='CASCADE'), nullable=False, index=True)
    stat_type = db.Column(db.String(100), nullable=False)
    stat_value = db.Column(db.Numeric, nullable=False)
    season = db.Column(db.String(20))

    athlete = db.relationship('Athlete', back_populates='stats')

    __table_args__ = (
        db.Index('idx_stats_athlete_season', 'athlete_id', 'season'),
    )

class AthleteMedia(BaseModel):
    __tablename__ = 'athlete_media'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id', ondelete='CASCADE'), nullable=False, index=True)
    media_type = db.Column(db.String(50))
    file_path = db.Column(db.String(255))
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    tags = db.Column(db.JSON)

    athlete = db.relationship('Athlete', back_populates='media')

    __table_args__ = (
        db.Index('idx_media_athlete_type', 'athlete_id', 'media_type'),
    )

class AthleteAchievement(BaseModel):
    __tablename__ = 'athlete_achievements'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id', ondelete='CASCADE'), nullable=False, index=True)
    achievement_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    date_achieved = db.Column(db.Date)

    athlete = db.relationship('Athlete', back_populates='achievements')

    __table_args__ = (
        db.Index('idx_achievements_athlete', 'athlete_id'),
    )
