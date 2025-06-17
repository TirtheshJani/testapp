import os
from app import create_app, db
from flask.cli import with_appcontext
import click

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    # Import models here to avoid circular imports
    from app.models import User, Role, AthleteProfile, Sport, Position
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'AthleteProfile': AthleteProfile,
        'Sport': Sport,
        'Position': Position
    }

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database with basic data."""
    from app.models import Role, Sport, Position
    
    db.create_all()
    
    # Create default roles
    roles = [
        {'name': 'admin', 'description': 'System Administrator'},
        {'name': 'agency_admin', 'description': 'Agency Administrator'},
        {'name': 'agent', 'description': 'Talent Agent'},
        {'name': 'scout', 'description': 'Talent Scout'},
        {'name': 'athlete', 'description': 'Professional Athlete'},
        {'name': 'viewer', 'description': 'Read-only Viewer'}
    ]
    
    for role_data in roles:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(
                name=role_data['name'],
                description=role_data['description'],
                is_system_role=True
            )
            db.session.add(role)
    
    # Create default sports
    sports = [
        {'name': 'Basketball', 'code': 'NBA'},
        {'name': 'Football', 'code': 'NFL'},
        {'name': 'Baseball', 'code': 'MLB'},
        {'name': 'Hockey', 'code': 'NHL'}
    ]
    
    for sport_data in sports:
        sport = Sport.query.filter_by(code=sport_data['code']).first()
        if not sport:
            sport = Sport(
                name=sport_data['name'],
                code=sport_data['code'],
                is_active=True
            )
            db.session.add(sport)
    
    db.session.commit()
    click.echo('Database initialized with default roles and sports.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)