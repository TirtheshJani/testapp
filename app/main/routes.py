from flask import render_template
from flask_login import current_user
from app.utils.auth import oauth_session_required
from app.main import bp

@bp.route('/')
def index():
    """Home page"""
    user_name = current_user.full_name if current_user.is_authenticated else None
    return render_template('main/index.html', user_name=user_name)

@bp.route('/dashboard')
@oauth_session_required
def dashboard():
    """User dashboard"""
    user_name = current_user.full_name
    return render_template('main/dashboard.html', user_name=user_name)
