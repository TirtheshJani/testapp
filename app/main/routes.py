from flask import render_template
from flask_login import current_user
from app.utils.auth import oauth_session_required
from app.main import bp

@bp.route('/')
def index():
    """Home page"""
    return render_template('main/index.html')

@bp.route('/dashboard')
@oauth_session_required
def dashboard():
    """User dashboard"""
    return render_template('main/dashboard.html')