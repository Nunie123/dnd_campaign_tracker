from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SearchField,
    TextAreaField,
    FloatField,
    SelectField,
)
from wtforms.validators import ValidationError, DataRequired, Length, Optional
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as _l
from app import db
from app.models import User


class SearchContent(FlaskForm):
    search_term = SearchField(("Search"), validators=[Length(min=0, max=128)])
    submit = SubmitField(_l("Search"))


class CreateCampaignForm(FlaskForm):
    name = StringField(
        _l("Campaign Name"), validators=[DataRequired(), Length(min=1, max=64)]
    )
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )
    setting = SelectField(_l("Setting", coerce=int))
    submit = SubmitField(_l("Create Campaign"))


class CreateSettingForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    geography_description = TextAreaField(
        _l("Geography"), validators=[Optional(), Length(min=0, max=1028)]
    )
    demographics_description = TextAreaField(
        _l("Demographics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    political_description = TextAreaField(
        _l("Politics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    economy_description = TextAreaField(
        _l("Economy"), validators=[Optional(), Length(min=0, max=1028)]
    )
    history_description = TextAreaField(
        _l("History"), validators=[Optional(), Length(min=0, max=1028)]
    )
    submit = SubmitField(_l("Submit"))


class CreateKingdomForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )
    ruler = StringField(_l("Ruler"), validators=[Optional(), Length(min=0, max=64)])
    geography_description = TextAreaField(
        _l("Geography"), validators=[Optional(), Length(min=0, max=1028)]
    )
    demographics_description = TextAreaField(
        _l("Demographics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    political_description = TextAreaField(
        _l("Politics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    economy_description = TextAreaField(
        _l("Economy"), validators=[Optional(), Length(min=0, max=1028)]
    )
    history_description = TextAreaField(
        _l("History"), validators=[Optional(), Length(min=0, max=1028)]
    )
    setting = SelectField(_l("Setting", coerce=int))
    submit = SubmitField(_l("Submit"))


class CreateCityForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )
    ruler = StringField(_l("Ruler"), validators=[Optional(), Length(min=0, max=64)])
    geography_description = TextAreaField(
        _l("Geography"), validators=[Optional(), Length(min=0, max=1028)]
    )
    demographics_description = TextAreaField(
        _l("Demographics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    political_description = TextAreaField(
        _l("Politics"), validators=[Optional(), Length(min=0, max=1028)]
    )
    economy_description = TextAreaField(
        _l("Economy"), validators=[Optional(), Length(min=0, max=1028)]
    )
    history_description = TextAreaField(
        _l("History"), validators=[Optional(), Length(min=0, max=1028)]
    )
    kingdom = SelectField(_l("Kingdom", coerce=int))
    setting = SelectField(_l("Setting", coerce=int))
    submit = SubmitField(_l("Submit"))


class CreatePointOfInterestForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )

    kingdom = SelectField(_l("Kingdom", coerce=int))
    setting = SelectField(_l("Setting", coerce=int))
    submit = SubmitField(_l("Submit"))


class CreateAdventureForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )
    quest_giver = StringField(
        _l("Name of Quest Giver"),
        validators=[Optional(), Length(min=1, max=128)],
    )
    reward = StringField(
        _l("Reward for Completing Adventure"),
        validators=[Optional(), Length(min=1, max=256)],
    )

    campaign = SelectField(_l("Campaign", coerce=int))
    submit = SubmitField(_l("Submit"))


class CreateEncounterForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(min=1, max=64)])
    short_description = StringField(
        _l("Tagline (1-3 sentence description)"),
        validators=[DataRequired(), Length(min=1, max=128)],
    )
    long_description = TextAreaField(
        _l("Description"),
        validators=[Optional(), Length(min=0, max=1028)],
    )
    challenge_rating = FloatField(_l("Challenge Rating"), validators=[Optional()])
    loot = StringField(
        _l("Loot"),
        validators=[Optional(), Length(min=0, max=128)],
    )

    campaign = SelectField(_l("Campaign", coerce=int))
    submit = SubmitField(_l("Submit"))
