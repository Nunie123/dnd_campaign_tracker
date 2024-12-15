from flask import Blueprint

bp = Blueprint("explore_assets", __name__)

from app.explore_assets import routes
