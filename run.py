import os
from app import create_app, db
from flask.cli import with_appcontext
import click

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database with basic data."""
    db.create_all()
    click.echo('Database initialized.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)