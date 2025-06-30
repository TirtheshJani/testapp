from app import db
from app.models.base import BaseModel

class NBATeam(BaseModel):
    __tablename__ = 'nba_teams'

    team_id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(10))
    city = db.Column(db.String(50))
    conference = db.Column(db.String(20))
    division = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    name = db.Column(db.String(100))

    games_home = db.relationship('NBAGame', back_populates='home_team', foreign_keys='NBAGame.home_team_id')
    games_away = db.relationship('NBAGame', back_populates='visitor_team', foreign_keys='NBAGame.visitor_team_id')

    def __repr__(self):
        return f'<NBATeam {self.full_name}>'


class MLBTeam(BaseModel):
    __tablename__ = 'mlb_teams'

    team_id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(10))
    name = db.Column(db.String(100))
    location = db.Column(db.String(50))
    league = db.Column(db.String(50))
    division = db.Column(db.String(50))

    def __repr__(self):
        return f'<MLBTeam {self.name}>'
