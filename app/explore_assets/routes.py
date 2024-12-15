from flask import render_template, request
import sqlalchemy as sa
from flask_babel import _

from app import db
from app.explore_assets.forms import SearchContent
from app.user.forms import EmptyForm
from app.models import Asset
from app.explore_assets import bp
from app.explore_assets.helpers import (
    get_asset_list_query,
    get_next_url,
    get_prev_url,
)


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    campaigns = db.paginate(
        sa.select(Asset)
        .filter(Asset.deleted_at.is_(None))
        .filter(Asset.asset_type == "campaign")
        .order_by(Asset.updated_at.desc()),  # TODO: order by popularity
        page=1,
        per_page=10,
        error_out=False,
    )
    settings = db.paginate(
        sa.select(Asset)
        .filter(Asset.deleted_at.is_(None))
        .filter(Asset.asset_type == "setting")
        .order_by(Asset.updated_at.desc()),  # TODO: order by popularity
        page=1,
        per_page=10,
        error_out=False,
    )
    return render_template(
        "index.html",
        title=_("Home"),
        campaigns=campaigns.items,
        settings=settings.items,
    )


@bp.route("/<asset_type>", defaults={"username": None}, methods=["GET", "POST"])
@bp.route("/<asset_type>/<username>", methods=["GET", "POST"])
def view_assets(asset_type, username):
    items_per_page = 6
    page = request.args.get("page", 1, type=int)
    form = SearchContent()
    if username:
        query = get_asset_list_query(asset_type, form, username)
    assets = db.paginate(query, page=page, per_page=items_per_page, error_out=False)
    next_url = get_next_url(assets, username, asset_type)
    prev_url = get_prev_url(assets, username, asset_type)
    return render_template(
        "assets/view_assets.html",
        title=_("Explore"),
        assets=assets.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
        username=username,
        asset_type=asset_type,
    )


@bp.route("/<asset_type>/<id>")
def view_asset_details(asset_type, id):
    asset = db.one_or_404(
        sa.select(Asset).filter(Asset.id == id, Asset.deleted_at.is_(None))
    )
    asset_fields = asset.get_asset_display_fields()
    form = EmptyForm()
    return render_template(
        "assets/view_asset_details.html",
        title=_(f"{asset_type} - {asset.name}"),
        asset=asset_fields,
        form=form,
    )


# @bp.route("/campaigns/<id>")
# def view_campaign_details(id):
#     asset = db.one_or_404(
#         sa.select(Campaign).filter(Campaign.id == id, Campaign.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_campaign_details.html",
#         title=_(f"Campaign - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/settings/<id>")
# def view_setting_details(id):
#     asset = db.one_or_404(
#         sa.select(Setting).filter(Setting.id == id, Setting.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_setting_details.html",
#         title=_(f"Setting - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/kingdoms/<id>")
# def view_kingdom_details(id):
#     asset = db.one_or_404(
#         sa.select(Kingdom).filter(Kingdom.id == id, Kingdom.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_kingdom_details.html",
#         title=_(f"Kingdom - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/cities/<id>")
# def view_city_details(id):
#     asset = db.one_or_404(
#         sa.select(City).filter(City.id == id, City.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_city_details.html",
#         title=_(f"City - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/points-of-interest/<id>")
# def view_point_of_interest_details(id):
#     asset = db.one_or_404(
#         sa.select(PointOfInterest).filter(
#             PointOfInterest.id == id, PointOfInterest.deleted_at.is_(None)
#         )
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_poi_details.html",
#         title=_(f"Point of Interest - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/adventures/<id>")
# def view_adventure_details(id):
#     asset = db.one_or_404(
#         sa.select(Adventure).filter(Adventure.id == id, Adventure.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_adventure_details.html",
#         title=_(f"Adventure - {asset.name}"),
#         asset=asset,
#         form=form,
#     )


# @bp.route("/encounters/<id>")
# def view_encounter_details(id):
#     asset = db.one_or_404(
#         sa.select(Encounter).filter(Encounter.id == id, Encounter.deleted_at.is_(None))
#     )
#     form = EmptyForm()
#     return render_template(
#         "explore/view_encounter_details.html",
#         title=_(f"Encounter - {asset.name}"),
#         asset=asset,
#         form=form,
#     )
