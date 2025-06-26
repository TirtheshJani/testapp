from flask import Blueprint, jsonify, abort
from app.models import AthleteProfile

bp = Blueprint('api', __name__)

@bp.route('/athletes/<string:athlete_id>')
def get_athlete(athlete_id):
    athlete = AthleteProfile.query.get(athlete_id)
    if not athlete:
        abort(404)
    return jsonify(athlete.to_dict())
