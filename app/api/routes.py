from flask import request, jsonify, send_file, abort
from app.api import bp
from app import db
from app.models import AthleteProfile, AthleteMedia, AthleteStat
from app.services.media_service import MediaService
from app.services.athlete_service import (
    create_athlete as create_athlete_service,
    get_athlete as get_athlete_service,
    update_athlete as update_athlete_service,
    delete_athlete as delete_athlete_service,
    list_athletes as list_athletes_service,
)

@bp.route('/athletes', methods=['POST'])
def create_athlete():
    data = request.get_json() or {}
    athlete = create_athlete_service(data)
    return jsonify(athlete.to_dict()), 201

@bp.route('/athletes/<athlete_id>', methods=['GET'])
def get_athlete(athlete_id):
    athlete = get_athlete_service(athlete_id)
    return jsonify(athlete.to_dict())

@bp.route('/athletes/<athlete_id>', methods=['PUT'])
def update_athlete(athlete_id):
    data = request.get_json() or {}
    athlete = update_athlete_service(athlete_id, data)
    return jsonify(athlete.to_dict())

@bp.route('/athletes/<athlete_id>', methods=['DELETE'])
def delete_athlete(athlete_id):
    delete_athlete_service(athlete_id)
    return '', 204

@bp.route('/athletes', methods=['GET'])
def list_athletes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = list_athletes_service(page, per_page)
    data = [a.to_dict() for a in pagination.items]
    return jsonify({'items': data, 'total': pagination.total})

# Media endpoints
@bp.route('/athletes/<athlete_id>/media', methods=['POST'])
def upload_media(athlete_id):
    athlete = AthleteProfile.query.get_or_404(athlete_id)
    if 'file' not in request.files:
        abort(400, 'No file provided')
    file = request.files['file']
    media_type = request.form.get('media_type', 'other')
    path, filename = MediaService.save_file(file, athlete_id, media_type)
    media = AthleteMedia(
        athlete_id=athlete_id,
        media_type=media_type,
        file_path=path,
        original_filename=file.filename,
    )
    db.session.add(media)
    db.session.commit()
    return jsonify(media.to_dict()), 201

@bp.route('/athletes/<athlete_id>/media', methods=['GET'])
def list_media(athlete_id):
    AthleteProfile.query.get_or_404(athlete_id)
    media = AthleteMedia.query.filter_by(athlete_id=athlete_id).all()
    return jsonify([m.to_dict() for m in media])

@bp.route('/media/<media_id>', methods=['DELETE'])
def delete_media(media_id):
    media = AthleteMedia.query.get_or_404(media_id)
    MediaService.delete_file(media.file_path)
    db.session.delete(media)
    db.session.commit()
    return '', 204

@bp.route('/media/<media_id>/download', methods=['GET'])
def download_media(media_id):
    media = AthleteMedia.query.get_or_404(media_id)
    return send_file(media.file_path, as_attachment=True, download_name=media.original_filename)

# Stats endpoints
@bp.route('/athletes/<athlete_id>/stats', methods=['POST'])
def add_or_update_stat(athlete_id):
    AthleteProfile.query.get_or_404(athlete_id)
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        abort(400, 'Missing stat name')
    stat = AthleteStat.query.filter_by(athlete_id=athlete_id, name=name).first()
    if stat:
        stat.value = data.get('value')
    else:
        stat = AthleteStat(athlete_id=athlete_id, name=name, value=data.get('value'))
        db.session.add(stat)
    db.session.commit()
    return jsonify(stat.to_dict())

@bp.route('/athletes/<athlete_id>/stats', methods=['GET'])
def get_stats(athlete_id):
    AthleteProfile.query.get_or_404(athlete_id)
    stats = AthleteStat.query.filter_by(athlete_id=athlete_id).all()
    return jsonify([s.to_dict() for s in stats])

@bp.route('/stats/<stat_id>', methods=['DELETE'])
def delete_stat(stat_id):
    stat = AthleteStat.query.get_or_404(stat_id)
    db.session.delete(stat)
    db.session.commit()
    return '', 204
