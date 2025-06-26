from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp

@bp.route('/')
def index():
    """Home page."""
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    return render_template('main/dashboard.html')


@bp.route('/athletes/<string:athlete_id>')
def athlete_view(athlete_id):
    """Page displaying a single athlete."""
    return render_template('main/athlete.html', athlete_id=athlete_id)
