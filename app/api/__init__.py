"""API blueprint setup."""

from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

# Import routes to register view functions with this blueprint
from app.api import routes  # noqa: E402
