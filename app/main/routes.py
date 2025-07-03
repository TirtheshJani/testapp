from flask import render_template, request
from flask_login import current_user
from sqlalchemy import func
from app import db
from app.models import AthleteProfile
from app.utils.auth import oauth_session_required
from app.main import bp

@bp.route('/')
def index():
    """Home page"""
    user_name = current_user.full_name if current_user.is_authenticated else None
    search_query = request.args.get('q', '')
    active_filter = request.args.get('filter', '')
    return render_template(
        'main/index.html',
        user_name=user_name,
        search_query=search_query,
        active_filter=active_filter,
    )

@bp.route('/dashboard')
@oauth_session_required
def dashboard():
    """User dashboard"""
    user_name = current_user.full_name
    total_athletes = (
        db.session.query(func.count(AthleteProfile.athlete_id))
        .filter(AthleteProfile.is_deleted.is_(False))
        .scalar()
    )
    active_contracts = (
        db.session.query(func.count(AthleteProfile.athlete_id))
        .filter(
            AthleteProfile.is_deleted.is_(False),
            AthleteProfile.contract_active.is_(True),
        )
        .scalar()
    )
    return render_template(
        'main/dashboard.html',
        user_name=user_name,
        total_athletes=total_athletes,
        active_contracts=active_contracts,
    )
