import sqlalchemy as sa
from flask import url_for

from app import db
from app.models import (
    Asset,
    User,
)


def get_asset_list_query(asset_type, form, username):
    # TODO: order by popularity
    user_id = db.session.scalar(
        sa.Select(User.id).filter(User.username == username, User.deleted_at.is_(None))
    )
    if form.validate_on_submit() and username:
        query = (
            sa.select(Asset)
            .filter(
                Asset.name.ilike(f"%{form.search_term.data}%"),
                Asset.owner_id == user_id,
                Asset.deleted_at.is_(None),
                Asset.asset_type == asset_type,
            )
            .order_by(Asset.updated_at.desc())
        )
    elif form.validate_on_submit():
        query = (
            sa.select(Asset)
            .filter(
                Asset.name.ilike(f"%{form.search_term.data}%"),
                Asset.deleted_at.is_(None),
                Asset.asset_type == asset_type,
            )
            .order_by(Asset.updated_at.desc())
        )
    elif username:
        query = (
            sa.select(Asset)
            .filter(
                Asset.owner_id == user_id,
                Asset.deleted_at.is_(None),
                Asset.asset_type == asset_type,
            )
            .order_by(Asset.updated_at.desc())
        )
    else:
        query = (
            sa.select(Asset)
            .filter(
                Asset.deleted_at.is_(None),
                Asset.asset_type == asset_type,
            )
            .order_by(Asset.updated_at.desc())
        )

    return query


def get_next_url(asset_object, username, asset_type):
    if asset_object.has_next:
        url = url_for(
            f"explore.view_assets",
            page=asset_object.next_num,
            username=username,
            asset_type=asset_type,
        )
    else:
        url = None
    return url


def get_prev_url(asset_object, username, asset_type):
    if asset_object.has_prev:
        url = url_for(
            f"explore.view_assets",
            page=asset_object.prev_num,
            username=username,
            asset_type=asset_type,
        )
    else:
        url = None
    return url


# def get_asset_type_details(asset_type: str):
#     asset_mapper = {
#         "campaign": {
#             "model": Campaign,
#             "create_form": CreateCampaignForm,
#             "create_url": "explore/create_campaign.html",
#         },
#         "setting": {
#             "model": Setting,
#             "create_form": CreateSettingForm,
#             "create_url": "explore/create_setting.html",
#         },
#         "kingdom": {
#             "model": Kingdom,
#             "create_form": CreateKingdomForm,
#             "create_url": "explore/create_kingdom.html",
#         },
#         "city": {
#             "model": City,
#             "create_form": CreateCityForm,
#             "create_url": "explore/create_city.html",
#         },
#         "point_of_interest": {
#             "model": PointOfInterest,
#             "create_form": CreatePointOfInterestForm,
#             "create_url": "explore/create_point_of_interest.html",
#         },
#         "adventure": {
#             "model": Adventure,
#             "create_form": CreateAdventureForm,
#             "create_url": "explore/create_adventure.html",
#         },
#         "encounter": {
#             "model": Encounter,
#             "create_form": CreateEncounterForm,
#             "create_url": "explore/create_encounter.html",
#         },
#     }
#     return asset_mapper.get(asset_type)
