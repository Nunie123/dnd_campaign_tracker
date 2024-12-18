import sqlalchemy as sa
from flask import url_for

from app import db
from app.models import (
    Campaign,
    Setting,
    Kingdom,
    City,
    PointOfInterest,
    Adventure,
    Encounter,
    User,
)
from app.assets.forms import (
    CreateCampaignForm,
    CreateCityForm,
    CreateEncounterForm,
    CreateKingdomForm,
    CreatePointOfInterestForm,
    CreateAdventureForm,
    CreateSettingForm,
)


def get_asset_list_query(model, form, username):
    # TODO: order by popularity
    user_id = db.session.scalar(
        sa.Select(User.id).filter(User.username == username, User.deleted_at.is_(None))
    )
    if form.validate_on_submit() and username:
        query = (
            sa.select(model)
            .filter(
                model.name.ilike(f"%{form.search_term.data}%"),
                model.owner_id == user_id,
                model.deleted_at.is_(None),
            )
            .order_by(model.updated_at.desc())
        )
    elif form.validate_on_submit():
        query = (
            sa.select(model)
            .filter(
                model.name.ilike(f"%{form.search_term.data}%"),
                model.deleted_at.is_(None),
            )
            .order_by(model.updated_at.desc())
        )
    elif username:
        query = (
            sa.select(model)
            .filter(model.owner_id == user_id, model.deleted_at.is_(None))
            .order_by(model.updated_at.desc())
        )
    else:
        query = (
            sa.select(model)
            .filter(model.deleted_at.is_(None))
            .order_by(model.updated_at.desc())
        )

    return query


def get_next_url(asset_object, username, asset_type):
    if asset_object.has_next:
        url = url_for(
            "assets.view_assets",
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
            "assets.view_assets",
            page=asset_object.prev_num,
            username=username,
            asset_type=asset_type,
        )
    else:
        url = None
    return url


def get_asset_type_details(asset_type: str):
    asset_mapper = {
        "campaign": {
            "model": Campaign,
            "create_form": CreateCampaignForm,
            "create_url": "assets/update_assets/update_campaign.html",
        },
        "setting": {
            "model": Setting,
            "create_form": CreateSettingForm,
            "create_url": "assets/update_assets/update_setting.html",
        },
        "kingdom": {
            "model": Kingdom,
            "create_form": CreateKingdomForm,
            "create_url": "assets/update_assets/update_kingdom.html",
        },
        "city": {
            "model": City,
            "create_form": CreateCityForm,
            "create_url": "assets/update_assets/update_city.html",
        },
        "point_of_interest": {
            "model": PointOfInterest,
            "create_form": CreatePointOfInterestForm,
            "create_url": "assets/update_assets/update_point_of_interest.html",
        },
        "adventure": {
            "model": Adventure,
            "create_form": CreateAdventureForm,
            "create_url": "assets/update_assets/update_adventure.html",
        },
        "encounter": {
            "model": Encounter,
            "create_form": CreateEncounterForm,
            "create_url": "assets/update_assets/update_encounter.html",
        },
    }
    return asset_mapper.get(asset_type)
