from app.update_assets import forms


def get_select_dropdown_choices(asset_type):
    model = get_asset_type_details(asset_type)["model"]
    asset_list = db.session.execute(
        sa.select(model.id, model.name)
        .filter(model.owner == current_user, model.deleted_at.is_(None))
        .order_by(model.name)
    ).all()
    choices = [(None, f"Select a {asset_type} later.")]
    choices.extend(
        [(asset.id, asset.name) for asset in asset_list] if asset_list else []
    )
    return choices


def get_update_form(asset_type):
    mapper = {
        "campaign": forms.CreateCampaignForm,
        "setting": forms.CreateSettingForm,
        "kingdom": forms.CreateKingdomForm,
        "city": forms.CreateCityForm,
        "point_of_interest": forms.CreatePointOfInterestForm,
        "adventure": forms.CreateAdventureForm,
        "encounter": forms.CreateEncounterForm,
    }
    return mapper[asset_type]
