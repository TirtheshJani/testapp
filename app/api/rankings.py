from flask import jsonify, current_app
from flask_restx import Resource
import json
import os

from app.api import api


_DEFAULT_RANKINGS = [
    {"name": "LeBron James", "score": 98.5},
    {"name": "Connor McDavid", "score": 97.8},
    {"name": "Mike Trout", "score": 96.2},
    {"name": "Aaron Donald", "score": 95.7},
    {"name": "Stephen Curry", "score": 94.9},
]


def _load_rankings():
    """Load rankings from file if configured, otherwise return defaults."""
    path = current_app.config.get("TOP_RANKINGS_FILE")
    if path and os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            current_app.logger.exception("Failed to load rankings file %s", path)
    return _DEFAULT_RANKINGS


@api.route('/rankings/top')
class TopRankings(Resource):
    """Return the top 5 athlete rankings with placeholder scores."""

    def get(self):
        return jsonify(_load_rankings())
