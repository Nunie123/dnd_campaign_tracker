from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    SearchField,
)
from wtforms.validators import Length
from flask_babel import _, lazy_gettext as _l


class SearchContent(FlaskForm):
    search_term = SearchField(("Search"), validators=[Length(min=0, max=128)])
    submit = SubmitField(_l("Search"))
