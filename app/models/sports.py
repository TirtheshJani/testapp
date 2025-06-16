from app import db
from app.models.base import BaseModel

class Sport(BaseModel):
    __tablename__ = 'sports'
    
    sport_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)  # NBA, NFL, MLB, NHL
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Sport {self.name}>'

class Position(BaseModel):
    __tablename__ = 'positions'
    
    position_id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.sport_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)  # PG, SG, SF, PF, C for basketball
    description = db.Column(db.Text)
    
    # Unique constraint per sport
    __table_args__ = (
        db.UniqueConstraint('sport_id', 'code', name='uq_sport_position_code'),
    )
    
    def __repr__(self):
        return f'<Position {self.name}>'