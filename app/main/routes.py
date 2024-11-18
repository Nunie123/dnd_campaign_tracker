from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
import sqlalchemy as sa

# from langdetect import detect, LangDetectException
from app import db
from app.main.forms import EditProfileForm, EmptyForm
from app.models import User, Campaign, Setting
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale())


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    campaigns = db.paginate(
        sa.select(Campaign)
        .filter(Campaign.deleted_at.is_(None))
        .order_by(Campaign.updated_at.desc()),  # TODO: order by popularity
        page=1,
        per_page=10,
        error_out=False,
    )
    settings = db.paginate(
        sa.select(Setting)
        .filter(Setting.deleted_at.is_(None))
        .order_by(Setting.updated_at.desc()),  # TODO: order by popularity
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


@bp.route("/user/<username>")
def user(username):
    user = db.first_or_404(
        sa.select(User)
        .filter(User.deleted_at.is_(None))
        .where(User.username == username)
    )
    form = EmptyForm()
    return render_template(
        "user.html",
        user=user,
        form=form,
    )


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_("Your changes have been saved."))
        return redirect(url_for("main.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title=_("Edit Profile"), form=form)


@bp.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot follow yourself!"))
            return redirect(url_for("main.user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_("You are following %(username)s!", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))


@bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(_("User %(username)s not found.", username=username))
            return redirect(url_for("main.index"))
        if user == current_user:
            flash(_("You cannot unfollow yourself!"))
            return redirect(url_for("main.user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_("You are not following %(username)s.", username=username))
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))


@bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    data = request.get_json()
    return {
        "text": translate(data["text"], data["source_language"], data["dest_language"])
    }
