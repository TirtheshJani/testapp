from app import db
from app.models.base import BaseModel
import uuid

class AthleteStat(BaseModel):
    __tablename__ = 'athlete_stats'

    stat_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    athlete_id = db.Column(db.String(36), db.ForeignKey('athlete_profiles.athlete_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100))

    athlete = db.relationship('AthleteProfile', backref='stats')

    __table_args__ = (
        db.Index('idx_stats_athlete', 'athlete_id'),
    )

    def __repr__(self):
        return f'<AthleteStat {self.stat_id}>'
