import os
from app import create_app, db
from app.models import (
    User,
    Role,
    UserRole,
    UserOAuthAccount,
    Sport,
    Position,
    AthleteProfile,
    AthleteSkill,
    AthleteStat,
)
from flask.cli import with_appcontext
import click
from datetime import date

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'UserRole': UserRole,
        'UserOAuthAccount': UserOAuthAccount,
        'Sport': Sport,
        'Position': Position,
        'AthleteProfile': AthleteProfile,
        'AthleteSkill': AthleteSkill,
        'AthleteStat': AthleteStat,
    }

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize database with default data"""
    db.create_all()
    
    # Create default roles
    roles_data = [
        {'name': 'admin', 'description': 'System Administrator'},
        {'name': 'agency_admin', 'description': 'Agency Administrator'},
        {'name': 'agent', 'description': 'Talent Agent'},
        {'name': 'scout', 'description': 'Talent Scout'},
        {'name': 'athlete', 'description': 'Professional Athlete'},
        {'name': 'viewer', 'description': 'Read-only Viewer'}
    ]
    
    for role_data in roles_data:
        if not Role.query.filter_by(name=role_data['name']).first():
            role = Role(
                name=role_data['name'],
                description=role_data['description'],
                is_system_role=True
            )
            db.session.add(role)
    
    # Create sports and positions
    sports_data = [
        {
            'name': 'Basketball',
            'code': 'NBA',
            'description': 'National Basketball Association',
            'positions': [
                {'name': 'Point Guard', 'code': 'PG', 'description': 'Primary ball handler'},
                {'name': 'Shooting Guard', 'code': 'SG', 'description': 'Perimeter shooter'},
                {'name': 'Small Forward', 'code': 'SF', 'description': 'Versatile wing player'},
                {'name': 'Power Forward', 'code': 'PF', 'description': 'Strong inside player'},
                {'name': 'Center', 'code': 'C', 'description': 'Primary post player'}
            ]
        },
        {
            'name': 'Football',
            'code': 'NFL',
            'description': 'National Football League',
            'positions': [
                {'name': 'Quarterback', 'code': 'QB', 'description': 'Field general'},
                {'name': 'Running Back', 'code': 'RB', 'description': 'Ball carrier'},
                {'name': 'Wide Receiver', 'code': 'WR', 'description': 'Pass catcher'},
                {'name': 'Tight End', 'code': 'TE', 'description': 'Receiver/blocker'},
                {'name': 'Offensive Line', 'code': 'OL', 'description': 'Blockers'}
            ]
        },
        {
            'name': 'Baseball',
            'code': 'MLB',
            'description': 'Major League Baseball',
            'positions': [
                {'name': 'Pitcher', 'code': 'P', 'description': 'Throws to batters'},
                {'name': 'Catcher', 'code': 'C', 'description': 'Receives pitches'},
                {'name': 'First Base', 'code': '1B', 'description': 'First base position'},
                {'name': 'Second Base', 'code': '2B', 'description': 'Second base position'},
                {'name': 'Shortstop', 'code': 'SS', 'description': 'Between 2nd and 3rd base'}
            ]
        },
        {
            'name': 'Hockey',
            'code': 'NHL',
            'description': 'National Hockey League',
            'positions': [
                {'name': 'Center', 'code': 'C', 'description': 'Forward center'},
                {'name': 'Left Wing', 'code': 'LW', 'description': 'Left wing forward'},
                {'name': 'Right Wing', 'code': 'RW', 'description': 'Right wing forward'},
                {'name': 'Defenseman', 'code': 'D', 'description': 'Defensive player'},
                {'name': 'Goaltender', 'code': 'G', 'description': 'Goal keeper'}
            ]
        },
        {
            'name': 'Soccer',
            'code': 'SOC',
            'description': 'International Federation of Association Football',
            'positions': [
                {'name': 'Forward', 'code': 'FW', 'description': 'Primary attacker'},
                {'name': 'Midfielder', 'code': 'MF', 'description': 'Midfield player'},
                {'name': 'Defender', 'code': 'DF', 'description': 'Defensive player'},
                {'name': 'Goalkeeper', 'code': 'GK', 'description': 'Goal keeper'}
            ]
        }
    ]
    
    for sport_data in sports_data:
        sport = Sport.query.filter_by(code=sport_data['code']).first()
        if not sport:
            sport = Sport(
                name=sport_data['name'],
                code=sport_data['code'],
                description=sport_data['description'],
                is_active=True
            )
            db.session.add(sport)
            db.session.flush()  # Get the sport ID
            
            # Add positions
            for pos_data in sport_data['positions']:
                position = Position(
                    sport_id=sport.sport_id,
                    name=pos_data['name'],
                    code=pos_data['code'],
                    description=pos_data['description']
                )
                db.session.add(position)

    # Commit roles, sports and positions
    db.session.commit()

    # Sample athlete with skills
    if not User.query.filter_by(username='sampleathlete').first():
        user = User(
            username='sampleathlete',
            email='sample@example.com',
            first_name='Sample',
            last_name='Athlete'
        )
        user.set_password('password')
        db.session.add(user)
        db.session.flush()

        profile = AthleteProfile(
            user_id=user.user_id,
            date_of_birth=date(1990, 1, 1)
        )
        db.session.add(profile)
        db.session.flush()

        skills = [
            AthleteSkill(athlete_id=profile.athlete_id, name='Speed', level=5),
            AthleteSkill(athlete_id=profile.athlete_id, name='Agility', level=4),
        ]
        db.session.add_all(skills)

    db.session.commit()
    click.echo('Database initialized with default roles, sports and sample athlete.')


@app.cli.command()
@with_appcontext
def seed_demo():
    """Insert demo users and athlete data."""
    from datetime import date

    # Ensure base tables and reference data exist
    init_db()

    demo_users = [
        {
            'username': 'ljames',
            'email': 'lebron@example.com',
            'first_name': 'LeBron',
            'last_name': 'James',
            'dob': date(1984, 12, 30),
            'sport': 'NBA',
            'position': 'SF',
            'nationality': 'USA',
            'skills': [
                {'name': 'Playmaking', 'level': 'expert'},
                {'name': 'Scoring', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'PPG', 'value': '27.0'},
                {'name': 'RPG', 'value': '7.4'},
            ],
        },
        {
            'username': 'tbrady',
            'email': 'brady@example.com',
            'first_name': 'Tom',
            'last_name': 'Brady',
            'dob': date(1977, 8, 3),
            'sport': 'NFL',
            'position': 'QB',
            'nationality': 'USA',
            'skills': [
                {'name': 'Passing', 'level': 'expert'},
                {'name': 'Leadership', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'TDs', 'value': '649'},
            ],
        },
        {
            'username': 'scrosby',
            'email': 'crosby@example.com',
            'first_name': 'Sidney',
            'last_name': 'Crosby',
            'dob': date(1987, 8, 7),
            'sport': 'NHL',
            'position': 'C',
            'nationality': 'CAN',
            'skills': [
                {'name': 'Stickhandling', 'level': 'expert'},
                {'name': 'Vision', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'Points', 'value': '1525'},
            ],
        },
        {
            'username': 'cmcdavid',
            'email': 'mcdavid@example.com',
            'first_name': 'Connor',
            'last_name': 'McDavid',
            'dob': date(1997, 1, 13),
            'sport': 'NHL',
            'position': 'C',
            'nationality': 'CAN',
            'skills': [
                {'name': 'Speed', 'level': 'expert'},
                {'name': 'Playmaking', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'Points', 'value': '153'},
            ],
        },
        {
            'username': 'mtrout',
            'email': 'trout@example.com',
            'first_name': 'Mike',
            'last_name': 'Trout',
            'dob': date(1991, 8, 7),
            'sport': 'MLB',
            'position': '1B',
            'nationality': 'USA',
            'skills': [
                {'name': 'Power', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'BattingAverage', 'value': '0.304'},
            ],
        },
        {
            'username': 'adonald',
            'email': 'donald@example.com',
            'first_name': 'Aaron',
            'last_name': 'Donald',
            'dob': date(1991, 5, 23),
            'sport': 'NFL',
            'position': 'OL',
            'nationality': 'USA',
            'skills': [
                {'name': 'Strength', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'PassingYards', 'value': '0'},
            ],
        },
        {
            'username': 'scurry',
            'email': 'curry@example.com',
            'first_name': 'Stephen',
            'last_name': 'Curry',
            'dob': date(1988, 3, 14),
            'sport': 'NBA',
            'position': 'PG',
            'nationality': 'USA',
            'skills': [
                {'name': 'Shooting', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'PPG', 'value': '24.6'},
            ],
        },
        {
            'username': 'giannis',
            'email': 'giannis@example.com',
            'first_name': 'Giannis',
            'last_name': 'Antetokounmpo',
            'dob': date(1994, 12, 6),
            'sport': 'NBA',
            'position': 'PF',
            'nationality': 'GRC',
            'skills': [
                {'name': 'Athleticism', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'PPG', 'value': '30.2'},
            ],
        },
        {
            'username': 'pmahomes',
            'email': 'mahomes@example.com',
            'first_name': 'Patrick',
            'last_name': 'Mahomes',
            'dob': date(1995, 9, 17),
            'sport': 'NFL',
            'position': 'QB',
            'nationality': 'USA',
            'skills': [
                {'name': 'Passing', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'PassingYards', 'value': '5250'},
            ],
        },
        {
            'username': 'sohtani',
            'email': 'ohtani@example.com',
            'first_name': 'Shohei',
            'last_name': 'Ohtani',
            'dob': date(1994, 7, 5),
            'sport': 'MLB',
            'position': 'P',
            'nationality': 'JPN',
            'skills': [
                {'name': 'Two-Way', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'BattingAverage', 'value': '0.304'},
            ],
        },
        {
            'username': 'lmessi',
            'email': 'messi@example.com',
            'first_name': 'Lionel',
            'last_name': 'Messi',
            'dob': date(1987, 6, 24),
            'sport': 'SOC',
            'position': 'FW',
            'nationality': 'ARG',
            'skills': [
                {'name': 'Dribbling', 'level': 'expert'},
            ],
            'stats': [
                {'name': 'Goals', 'value': '30'},
            ],
        },
    ]

    for info in demo_users:
        if User.query.filter_by(username=info['username']).first():
            continue

        user = User(
            username=info['username'],
            email=info['email'],
            first_name=info['first_name'],
            last_name=info['last_name'],
        )
        db.session.add(user)
        db.session.flush()

        sport = Sport.query.filter_by(code=info['sport']).first()
        position = None
        if sport:
            position = Position.query.filter_by(
                sport_id=sport.sport_id, code=info['position']
            ).first()

        profile = AthleteProfile(
            user_id=user.user_id,
            primary_sport_id=sport.sport_id if sport else None,
            primary_position_id=position.position_id if position else None,
            date_of_birth=info['dob'],
            nationality=info['nationality'],
        )
        db.session.add(profile)
        db.session.flush()

        for sk in info['skills']:
            db.session.add(
                AthleteSkill(
                    athlete_id=profile.athlete_id,
                    name=sk['name'],
                    level=sk['level'],
                )
            )

        for st in info['stats']:
            db.session.add(
                AthleteStat(
                    athlete_id=profile.athlete_id,
                    name=st['name'],
                    value=st['value'],
                )
            )

    db.session.commit()
    click.echo('Demo athlete data created.')


@app.cli.command('backfill-stats')
@click.option('--seasons', default=3, type=int, help='Number of past seasons to backfill')
@with_appcontext
def backfill_stats_cmd(seasons: int):
    """Backfill historical statistics for all athletes."""
    from app import jobs
    jobs.historical_backfill_stats(num_seasons=seasons)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
