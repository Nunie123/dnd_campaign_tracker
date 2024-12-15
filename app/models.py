from datetime import datetime, timezone, date
from hashlib import md5
from time import time
from typing import Optional, List, Literal, get_args
import enum

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import true, false
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app import db, login


followers = sa.Table(
    "followers",
    db.metadata,
    sa.Column("follower_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("followed_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140), nullable=True)
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=false())

    # campaigns: so.Mapped[List["Campaign"]] = so.relationship(back_populates="owner")
    # settings: so.Mapped[List["Setting"]] = so.relationship(back_populates="owner")
    # sessions: so.Mapped[List["Session"]] = so.relationship(back_populates="game_master")
    # kingdoms: so.Mapped[List["Kingdom"]] = so.relationship(back_populates="owner")
    # cities: so.Mapped[List["City"]] = so.relationship(back_populates="owner")
    # points_of_interest: so.Mapped[List["PointOfInterest"]] = so.relationship(
    #     back_populates="owner"
    # )
    # adventures: so.Mapped[List["Adventure"]] = so.relationship(back_populates="owner")
    # encounters: so.Mapped[List["Encounter"]] = so.relationship(back_populates="owner")
    # religions: so.Mapped[List["Religion"]] = so.relationship(back_populates="owner")

    following: so.WriteOnlyMapped["User"] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates="followers",
    )
    followers: so.WriteOnlyMapped["User"] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates="following",
    )

    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery()
        )
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery()
        )
        return db.session.scalar(query)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except Exception:
            return
        return db.session.get(User, id)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# ASSET_TYPES = [
#     "setting",
#     "campaign",
#     "adventure",
#     "city",
#     "encounter",
#     "kingdom",
#     "point_of_interest",
#     "creature",
#     "spell",
#     "item",
#     "feat",
# ]
# ASSET_ENUM_TYPE = Literal[*ASSET_TYPES]


class AssetTypes(enum.Enum):
    setting = enum.auto()
    campaign = enum.auto()
    adventure = enum.auto()
    city = enum.auto()
    encounter = enum.auto()
    kingdom = enum.auto()
    point_of_interest = enum.auto()
    creature = enum.auto()
    spell = enum.auto()
    item = enum.auto()
    feat = enum.auto()


class Asset(db.Model):
    __tablename__ = "asset"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    asset_type: so.Mapped[AssetTypes] = so.mapped_column(sa.Enum(AssetTypes))

    # Descriptions
    short_description: so.Mapped[str] = so.mapped_column(sa.String(256))
    long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
    geography_description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    demographics_description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    political_description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    economy_description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    history_description: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256), nullable=True
    )
    gm_notes: so.Mapped[str] = so.mapped_column(sa.String(2000), nullable=True)

    # City/Kingdom fields
    ruler: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)

    # Religion fields
    diety_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    symbol_description: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)

    # Adventure fields
    quest_giver: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    reward: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)

    # Encounter fields
    challenge_rating: so.Mapped[int] = so.mapped_column(sa.Float, nullable=True)
    loot: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=True)

    # Flags
    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
    needs_review: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=false())

    # Timestamps
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    # Owner
    owner: so.Mapped[User] = so.relationship(back_populates="settings")
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # References
    setting: so.Mapped["Asset"] = so.relationship("Asset", remote_side=[id])
    setting_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("asset.id"), index=True, nullable=True
    )
    settings: so.Mapped[List["Asset"]] = so.relationship(
        "Asset", back_populates="setting"
    )

    campaign: so.Mapped["Asset"] = so.relationship("Asset", remote_side=[id])
    campaign_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("asset.id"), index=True, nullable=True
    )
    campaigns: so.Mapped[List["Asset"]] = so.relationship(
        "Asset", back_populates="campaign"
    )

    kingdom: so.Mapped["Asset"] = so.relationship("Asset", remote_side=[id])
    kingdom_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("asset.id"), index=True, nullable=True
    )
    kingdoms: so.Mapped[List["Asset"]] = so.relationship(
        "Asset", back_populates="kingdom"
    )

    def __repr__(self):
        return f"<Asset {self.asset_type}: {self.name}>"

    def get_asset_display_fields(self):
        fields = {
            "Name": self.name,
            "Created By": self.owner,
            "Tagline": self.short_description,
            "Description": self.long_description,
        }
        if self.asset_type in [
            "campaign",
            "setting",
            "kingdom",
            "city",
            "point_of_interest",
        ]:
            fields["Geogrphy"] = self.geography_description
            fields["Demographics"] = self.demographics_description
            fields["Politics"] = self.political_description
            fields["Economy"] = self.economy_description
            fields["History"] = self.history_description
        if self.asset_type in ["campaign", "encounter"]:
            fields["GM Notes (only visible to you)"] = self.gm_notes
        if self.asset_type in ["city", "kingdom"]:
            fields["Ruler"] = self.ruler
        if self.asset_type == "religion":
            fields["Diety"] = self.diety_name
            fields["Holy Symbols"] = self.symbol_description
        if self.asset_type == "adventure":
            fields["Quest Giver"] = self.quest_giver
            fields["Reward"] = self.reward
            fields["Campaign"] = self.campaign
        if self.asset_type == "encounter":
            fields["Challenge Rating"] = self.challenge_rating
            fields["Loot"] = self.loot
            fields["Campaign"] = self.campaign
        if self.asset_type in [
            "campaign",
            "kingdom",
            "city",
            "point_of_interest",
            "religion",
        ]:
            fields["Setting"] = self.setting
        if self.asset_type in ["city", "point_of_interest"]:
            fields["Kingdom"] = self.kingdom


class Session(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    session_date: so.Mapped[date] = so.mapped_column(sa.Date)
    players: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    short_description: so.Mapped[str] = so.mapped_column(sa.String(128))
    long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)

    game_master: so.Mapped[User] = so.relationship(back_populates="sessions")
    game_master_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id), index=True
    )

    language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5))

    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    def __repr__(self):
        return "<Session {}>".format(self.session_date)


# class Setting(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(128))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(256))
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
#     geography_description: so.Mapped[Optional[str]] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     demographics_description: so.Mapped[Optional[str]] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     political_description: so.Mapped[Optional[str]] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     economy_description: so.Mapped[Optional[str]] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     history_description: so.Mapped[Optional[str]] = so.mapped_column(
#         sa.String(256), nullable=True
#     )

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     owner: so.Mapped[User] = so.relationship(back_populates="settings")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     campaigns: so.Mapped[List["Campaign"]] = so.relationship(back_populates="setting")
#     kingdoms: so.Mapped[List["Kingdom"]] = so.relationship(back_populates="setting")
#     religions: so.Mapped[List["Religion"]] = so.relationship(back_populates="setting")
#     cities: so.Mapped[List["City"]] = so.relationship(back_populates="setting")
#     points_of_interest: so.Mapped[List["PointOfInterest"]] = so.relationship(
#         back_populates="setting"
#     )

#     def __repr__(self):
#         return "<Setting {}>".format(self.name)


# class Campaign(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(128))
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(2000), nullable=True)
#     gm_notes: so.Mapped[str] = so.mapped_column(sa.String(2000), nullable=True)

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     owner: so.Mapped[User] = so.relationship(back_populates="campaigns")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     setting: so.Mapped[Setting] = so.relationship(back_populates="campaigns")
#     setting_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Setting.id), index=True, nullable=True
#     )

#     adventures: so.Mapped[List["Adventure"]] = so.relationship(
#         back_populates="campaign"
#     )
#     encounters: so.Mapped[List["Encounter"]] = so.relationship(
#         back_populates="campaign"
#     )

#     def __repr__(self):
#         return "<Campaign {}>".format(self.name)


# class Kingdom(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(128))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
#     ruler: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
#     geography_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     demographics_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     political_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     economy_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     history_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5))

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     setting: so.Mapped[Setting] = so.relationship(back_populates="kingdoms")
#     setting_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Setting.id), index=True, nullable=True
#     )

#     cities: so.Mapped[List["City"]] = so.relationship(back_populates="kingdom")
#     points_of_interest: so.Mapped[List["PointOfInterest"]] = so.relationship(
#         back_populates="kingdom"
#     )

#     owner: so.Mapped[User] = so.relationship(back_populates="kingdoms")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     def __repr__(self):
#         return "<Kingdom {}>".format(self.name)


# class City(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(128))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
#     government_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     ruler: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
#     geography_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     demographics_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     political_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     economy_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     history_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     kingdom: so.Mapped[Kingdom] = so.relationship(back_populates="cities")
#     kingdom_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Kingdom.id), index=True, nullable=True
#     )

#     setting: so.Mapped[Setting] = so.relationship(back_populates="cities")
#     setting_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Setting.id), index=True, nullable=True
#     )

#     owner: so.Mapped[User] = so.relationship(back_populates="cities")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     def __repr__(self):
#         return "<City {}>".format(self.name)


# class PointOfInterest(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(128))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     kingdom: so.Mapped[Kingdom] = so.relationship(back_populates="points_of_interest")
#     kingdom_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Kingdom.id), index=True, nullable=True
#     )

#     setting: so.Mapped[Setting] = so.relationship(back_populates="points_of_interest")
#     setting_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Setting.id), index=True, nullable=True
#     )

#     owner: so.Mapped[User] = so.relationship(back_populates="points_of_interest")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     def __repr__(self):
#         return "<PointOfInterest {}>".format(self.name)


# class Religion(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(128))
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
#     diety_name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     symbol_description: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)
#     followers_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )
#     history_description: so.Mapped[str] = so.mapped_column(
#         sa.String(256), nullable=True
#     )

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     setting: so.Mapped[Setting] = so.relationship(back_populates="religions")
#     setting_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Setting.id), index=True)

#     owner: so.Mapped[User] = so.relationship(back_populates="religions")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     def __repr__(self):
#         return "<Religion {}>".format(self.name)


# class Adventure(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     quest_giver: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
#     reward: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(128))
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     owner: so.Mapped[User] = so.relationship(back_populates="adventures")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     campaign: so.Mapped[Campaign] = so.relationship(back_populates="adventures")
#     campaign_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Campaign.id), index=True, nullable=True
#     )

#     def __repr__(self):
#         return "<Adventure {}>".format(self.name)


# class Encounter(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)

#     name: so.Mapped[str] = so.mapped_column(sa.String(64))
#     challenge_rating: so.Mapped[int] = so.mapped_column(sa.Float, nullable=True)
#     short_description: so.Mapped[str] = so.mapped_column(sa.String(128))
#     long_description: so.Mapped[str] = so.mapped_column(sa.String(1028), nullable=True)
#     loot: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=True)

#     language: so.Mapped[Optional[str]] = so.mapped_column(sa.String(5), nullable=True)

#     is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=true())
#     created_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     updated_at: so.Mapped[datetime] = so.mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     deleted_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

#     owner: so.Mapped[User] = so.relationship(back_populates="encounters")
#     owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

#     campaign: so.Mapped[Campaign] = so.relationship(back_populates="encounters")
#     campaign_id: so.Mapped[int] = so.mapped_column(
#         sa.ForeignKey(Campaign.id), index=True, nullable=True
#     )

#     def __repr__(self):
#         return "<Encounter {}>".format(self.name)
