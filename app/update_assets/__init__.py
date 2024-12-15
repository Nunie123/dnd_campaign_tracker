from flask import Blueprint

bp = Blueprint("update_assets", __name__)

from app.update_assets import routes
