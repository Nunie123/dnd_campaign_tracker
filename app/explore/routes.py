# from datetime import datetime, timezone

# from flask import render_template, flash, redirect, url_for, request, g, current_app
# import sqlalchemy as sa
# from sqlalchemy.orm.session import make_transient
# from flask_babel import _, get_locale
# from flask_login import current_user, login_required

# from app import db
# from app.explore.forms import SearchContent
# from app.main.forms import EmptyForm
# from app.models import (
#     Campaign,
#     Setting,
#     Kingdom,
#     City,
#     PointOfInterest,
#     Adventure,
#     Encounter,
# )
# from app.explore import bp
# from app.explore.helpers import (
#     get_asset_list_query,
#     get_asset_type_details,
#     get_next_url,
#     get_prev_url,
# )


# @bp.route("/<asset_type>", defaults={"username": None}, methods=["GET", "POST"])
# @bp.route("/<asset_type>/<username>", methods=["GET", "POST"])
# def view_assets(asset_type, username):
#     items_per_page = 6
#     page = request.args.get("page", 1, type=int)
#     model = get_asset_type_details(asset_type)["model"]
#     form = SearchContent()
#     query = get_asset_list_query(model, form, username)
#     campaigns = db.paginate(query, page=page, per_page=items_per_page, error_out=False)
#     next_url = get_next_url(campaigns, username, asset_type)
#     prev_url = get_prev_url(campaigns, username, asset_type)
#     return render_template(
#         "explore/view_assets.html",
#         title=_("Explore Campaigns"),
#         assets=campaigns.items,
#         next_url=next_url,
#         prev_url=prev_url,
#         form=form,
#         username=username,
#         asset_type=asset_type,
#     )


# @bp.route("/<asset_type>/<id>/delete", methods=["POST"])
# def delete_asset(asset_type, id):
#     model = get_asset_type_details(asset_type)["model"]
#     asset = db.one_or_404(sa.select(model).filter(model.id == id))
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own."))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type=asset_type,
#                 username=current_user.username,
#             )
#         )
#     form = EmptyForm()
#     if form.validate_on_submit():
#         asset.deleted_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your {asset_type} has been deleted."))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type=asset_type,
#                 username=current_user.username,
#             )
#         )


# @bp.route("/<asset_type>/<id>/copy", methods=["POST"])
# def copy_asset(asset_type, id):
#     model = get_asset_type_details(asset_type)["model"]
#     asset = db.one_or_404(sa.select(model).filter(model.id == id))
#     if asset.owner.id == current_user.id:
#         flash(_(f"You can only copy assets that you don't already own."))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type=asset_type,
#                 username=current_user.username,
#             )
#         )
#     form = EmptyForm()
#     if form.validate_on_submit():
#         make_transient(asset)
#         asset._oid = None
#         asset.id = None
#         asset.owner = current_user
#         db.session.add(asset)
#         db.session.commit()
#         flash(_(f"This {asset_type} has been copied to your account."))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type=asset_type,
#                 username=current_user.username,
#             )
#         )


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


# def get_select_dropdown_choices(asset_type):
#     model = get_asset_type_details(asset_type)["model"]
#     asset_list = db.session.execute(
#         sa.select(model.id, model.name)
#         .filter(model.owner == current_user, model.deleted_at.is_(None))
#         .order_by(model.name)
#     ).all()
#     choices = [(None, f"Select a {asset_type} later.")]
#     choices.extend(
#         [(asset.id, asset.name) for asset in asset_list] if asset_list else []
#     )
#     return choices


# def create_asset(asset_type):
#     asset_details = get_asset_type_details(asset_type)
#     form = asset_details["create_form"]()
#     if hasattr(form, "setting"):
#         choices = get_select_dropdown_choices("setting")
#         form.setting.choices = choices
#     if hasattr(form, "campaign"):
#         choices = get_select_dropdown_choices("campaign")
#         form.campaign.choices = choices
#     if hasattr(form, "kingdom"):
#         choices = get_select_dropdown_choices("kingdom")
#         form.kingdom.choices = choices
#     if form.validate_on_submit():
#         new_asset = asset_details["model"](
#             name=form.name.data,
#             short_description=form.short_description.data,
#             owner=current_user,
#         )
#         if hasattr(form, "long_description"):
#             new_asset.long_description = form.long_description.data
#         if hasattr(form, "geography_description"):
#             new_asset.geography_description = form.geography_description.data
#         if hasattr(form, "demographics_description"):
#             new_asset.demographics_description = form.demographics_description.data
#         if hasattr(form, "political_description"):
#             new_asset.political_description = form.political_description.data
#         if hasattr(form, "economy_description"):
#             new_asset.economy_description = form.economy_description.data
#         if hasattr(form, "history_description"):
#             new_asset.history_description = form.history_description.data
#         if hasattr(form, "ruler"):
#             new_asset.ruler = form.ruler.data
#         if hasattr(form, "quest_giver"):
#             new_asset.quest_giver = form.quest_giver.data
#         if hasattr(form, "reward"):
#             new_asset.reward = form.reward.data
#         if hasattr(form, "challenge_rating"):
#             new_asset.challenge_rating = form.challenge_rating.data
#         if hasattr(form, "loot"):
#             new_asset.loot = form.loot.data

#         if hasattr(form, "setting"):
#             setting = db.session.scalar(
#                 sa.Select(Setting).where(
#                     Setting.id == form.setting.data, Setting.deleted_at.is_(None)
#                 )
#             )
#             new_asset.setting = setting
#         if hasattr(form, "campaign"):
#             campaign = db.session.scalar(
#                 sa.Select(Campaign).where(
#                     Campaign.id == form.campaign.data, Campaign.deleted_at.is_(None)
#                 )
#             )
#             new_asset.campaign = campaign
#         if hasattr(form, "kingdom"):
#             kingdom = db.session.scalar(
#                 sa.Select(Kingdom).where(
#                     Kingdom.id == form.kingdom.data, Kingdom.deleted_at.is_(None)
#                 )
#             )
#             new_asset.kingdom = kingdom
#         db.session.add(new_asset)
#         db.session.commit()
#         flash(_(f"Your {asset_type} has been created!"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type=asset_type,
#                 username=current_user.username,
#             )
#         )
#     return render_template(
#         asset_details["create_url"],
#         title=_(f"Create {asset_type.title()}"),
#         form=form,
#         form_type="Create",
#     )


# @bp.route("/campaigns/create", methods=["GET", "POST"])
# @login_required
# def create_campaign():
#     return create_asset("campaign")


# @bp.route("/settings/create", methods=["GET", "POST"])
# @login_required
# def create_setting():
#     return create_asset("setting")


# @bp.route("/kingdoms/create", methods=["GET", "POST"])
# @login_required
# def create_kingdom():
#     return create_asset("kingdom")


# @bp.route("/cities/create", methods=["GET", "POST"])
# @login_required
# def create_city():
#     return create_asset("city")


# @bp.route("/points-of-interest/create", methods=["GET", "POST"])
# @login_required
# def create_point_of_interest():
#     return create_asset("point_of_interest")


# @bp.route("/adventures/create", methods=["GET", "POST"])
# @login_required
# def create_adventure():
#     return create_asset("adventure")


# @bp.route("/encounters/create", methods=["GET", "POST"])
# @login_required
# def create_encounter():
#     return create_asset("encounter")


# @bp.route("/campaigns/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_campaign(id):
#     asset_details = get_asset_type_details("campaign")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     if asset.setting:
#         form = asset_details["create_form"](setting=asset.setting.id)
#     else:
#         form = asset_details["create_form"]()
#     form.setting.choices = get_select_dropdown_choices("setting")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.setting_id = form.setting.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Campaign has been updated."))
#         return redirect(url_for("explore.view_campaign_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         form.setting.data = asset.setting_id
#         form.submit.label.text = "Update Campaign"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Campaign"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/settings/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_setting(id):
#     asset_details = get_asset_type_details("setting")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     form = asset_details["create_form"]()
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.geography_description = form.geography_description.data
#         asset.demographics_description = form.demographics_description.data
#         asset.political_description = form.political_description.data
#         asset.economy_description = form.economy_description.data
#         asset.history_description = form.history_description.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Setting has been updated."))
#         return redirect(url_for("explore.view_setting_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.geography_description.data = asset.geography_description
#         form.demographics_description.data = asset.demographics_description
#         form.political_description.data = asset.political_description
#         form.economy_description.data = asset.economy_description
#         form.history_description.data = asset.history_description
#         form.submit.label.text = "Update Setting"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Setting"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/kingdoms/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_kingdom(id):
#     asset_details = get_asset_type_details("kingdom")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     if asset.setting:
#         form = asset_details["create_form"](setting=asset.setting.id)
#     else:
#         form = asset_details["create_form"]()
#     form.setting.choices = get_select_dropdown_choices("setting")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.ruler = form.ruler.data
#         asset.geography_description = form.geography_description.data
#         asset.demographics_description = form.demographics_description.data
#         asset.political_description = form.political_description.data
#         asset.economy_description = form.economy_description.data
#         asset.history_description = form.history_description.data
#         asset.setting_id = form.setting.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Kingdom has been updated."))
#         return redirect(url_for("explore.view_kingdom_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         form.ruler.data = asset.ruler
#         form.geography_description.data = asset.geography_description
#         form.demographics_description.data = asset.demographics_description
#         form.political_description.data = asset.political_description
#         form.economy_description.data = asset.economy_description
#         form.history_description.data = asset.history_description
#         asset.setting_id = form.setting.data
#         form.submit.label.text = "Update Kingdom"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Kingdom"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/cities/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_city(id):
#     asset_details = get_asset_type_details("city")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     if asset.setting and asset.kingdom:
#         form = asset_details["create_form"](
#             setting=asset.setting.id, kingdom=asset.kingdom.id
#         )
#     elif asset.setting:
#         form = asset_details["create_form"](setting=asset.setting.id)
#     elif asset.kingdom:
#         form = asset_details["create_form"](kingdom=asset.kingdom.id)
#     else:
#         form = asset_details["create_form"]()
#     form.setting.choices = get_select_dropdown_choices("setting")
#     form.kingdom.choices = get_select_dropdown_choices("kingdom")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.ruler = form.ruler.data
#         asset.geography_description = form.geography_description.data
#         asset.demographics_description = form.demographics_description.data
#         asset.political_description = form.political_description.data
#         asset.economy_description = form.economy_description.data
#         asset.history_description = form.history_description.data
#         asset.setting_id = form.setting.data
#         asset.kingdom_id = form.kingdom.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your City has been updated."))
#         return redirect(url_for("explore.view_city_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         form.ruler.data = asset.ruler
#         form.geography_description.data = asset.geography_description
#         form.demographics_description.data = asset.demographics_description
#         form.political_description.data = asset.political_description
#         form.economy_description.data = asset.economy_description
#         form.history_description.data = asset.history_description
#         asset.setting_id = form.setting.data
#         asset.kingdom_id = form.kingdom.data
#         form.submit.label.text = "Update City"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit City"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/points-of-interest/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_point_of_interest(id):
#     asset_details = get_asset_type_details("point_of_interest")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     if asset.setting and asset.kingdom:
#         form = asset_details["create_form"](
#             setting=asset.setting.id, kingdom=asset.kingdom.id
#         )
#     elif asset.setting:
#         form = asset_details["create_form"](setting=asset.setting.id)
#     elif asset.kingdom:
#         form = asset_details["create_form"](kingdom=asset.kingdom.id)
#     else:
#         form = asset_details["create_form"]()
#     form.setting.choices = get_select_dropdown_choices("setting")
#     form.kingdom.choices = get_select_dropdown_choices("kingdom")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.setting_id = form.setting.data
#         asset.kingdom_id = form.kingdom.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Point of Interest has been updated."))
#         return redirect(url_for("explore.view_point_of_interest_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         asset.setting_id = form.setting.data
#         asset.kingdom_id = form.kingdom.data
#         form.submit.label.text = "Update Point of Interest"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Point of Interest"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/adventures/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_adventure(id):
#     asset_details = get_asset_type_details("adventure")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="adventure",
#                 username=current_user.username,
#             )
#         )
#     if asset.campaign:
#         form = asset_details["create_form"](campaign=asset.campaign.id)
#     else:
#         form = asset_details["create_form"]()
#     form.campaign.choices = get_select_dropdown_choices("campaign")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.quest_giver = form.quest_giver.data
#         asset.reward = form.reward.data
#         asset.campaign_id = form.campaign.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Adventure has been updated."))
#         return redirect(url_for("explore.view_adventure_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         form.quest_giver.data = asset.quest_giver
#         form.reward.data = asset.reward
#         form.campaign.data = asset.campaign_id
#         form.submit.label.text = "Update Adventure"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Adventure"),
#         form=form,
#         form_type="Edit",
#     )


# @bp.route("/encounters/<id>/edit", methods=["GET", "POST"])
# @login_required
# def edit_encounter(id):
#     asset_details = get_asset_type_details("encounter")
#     model = asset_details["model"]
#     asset = db.one_or_404(
#         sa.Select(model).filter(model.id == id, model.deleted_at.is_(None))
#     )
#     if asset.owner.id != current_user.id:
#         flash(_(f"You can only edit assets that you own"))
#         return redirect(
#             url_for(
#                 "explore.view_assets",
#                 asset_type="campaign",
#                 username=current_user.username,
#             )
#         )
#     if asset.campaign:
#         form = asset_details["create_form"](campaign=asset.campaign.id)
#     else:
#         form = asset_details["create_form"]()
#     form.campaign.choices = get_select_dropdown_choices("campaign")
#     if form.validate_on_submit():
#         asset.name = form.name.data
#         asset.short_description = form.short_description.data
#         asset.long_description = form.long_description.data
#         asset.challenge_rating = form.challenge_rating.data
#         asset.loot = form.loot.data
#         asset.campaign_id = form.campaign.data
#         asset.updated_at = datetime.now(timezone.utc)
#         db.session.commit()
#         flash(_(f"Your Encounter has been updated."))
#         return redirect(url_for("explore.view_encounter_details", id=asset.id))
#     elif request.method == "GET":
#         form.name.data = asset.name
#         form.short_description.data = asset.short_description
#         form.long_description.data = asset.long_description
#         form.challenge_rating.data = asset.challenge_rating
#         form.loot.data = asset.loot
#         form.campaign.data = asset.campaign_id
#         form.submit.label.text = "Update Encounter"
#     return render_template(
#         asset_details["create_url"],
#         title=_("Edit Encounter"),
#         form=form,
#         form_type="Edit",
#     )
