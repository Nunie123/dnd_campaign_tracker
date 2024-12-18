"""empty message

Revision ID: 3a44041da450
Revises: 
Create Date: 2024-12-15 10:15:52.862996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a44041da450'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('session_date', sa.Date(), nullable=False),
    sa.Column('players', sa.String(length=256), nullable=True),
    sa.Column('short_description', sa.String(length=128), nullable=False),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('game_master_id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['game_master_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_session_game_master_id'), ['game_master_id'], unique=False)

    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('short_description', sa.String(length=256), nullable=False),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('geography_description', sa.String(length=256), nullable=True),
    sa.Column('demographics_description', sa.String(length=256), nullable=True),
    sa.Column('political_description', sa.String(length=256), nullable=True),
    sa.Column('economy_description', sa.String(length=256), nullable=True),
    sa.Column('history_description', sa.String(length=256), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('setting', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_setting_owner_id'), ['owner_id'], unique=False)

    op.create_table('campaign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('short_description', sa.String(length=128), nullable=False),
    sa.Column('long_description', sa.String(length=2000), nullable=True),
    sa.Column('gm_notes', sa.String(length=2000), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['setting.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('campaign', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_campaign_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_campaign_setting_id'), ['setting_id'], unique=False)

    op.create_table('kingdom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('short_description', sa.String(length=256), nullable=True),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('ruler', sa.String(length=64), nullable=True),
    sa.Column('geography_description', sa.String(length=256), nullable=True),
    sa.Column('demographics_description', sa.String(length=256), nullable=True),
    sa.Column('political_description', sa.String(length=256), nullable=True),
    sa.Column('economy_description', sa.String(length=256), nullable=True),
    sa.Column('history_description', sa.String(length=256), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['setting.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('kingdom', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_kingdom_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_kingdom_setting_id'), ['setting_id'], unique=False)

    op.create_table('religion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('short_description', sa.String(length=128), nullable=False),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('diety_name', sa.String(length=64), nullable=False),
    sa.Column('symbol_description', sa.String(length=128), nullable=True),
    sa.Column('followers_description', sa.String(length=256), nullable=True),
    sa.Column('history_description', sa.String(length=256), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['setting.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('religion', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_religion_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_religion_setting_id'), ['setting_id'], unique=False)

    op.create_table('adventure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('quest_giver', sa.String(length=64), nullable=True),
    sa.Column('reward', sa.String(length=256), nullable=True),
    sa.Column('short_description', sa.String(length=128), nullable=False),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('adventure', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_adventure_campaign_id'), ['campaign_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_adventure_owner_id'), ['owner_id'], unique=False)

    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('short_description', sa.String(length=256), nullable=True),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('government_description', sa.String(length=256), nullable=True),
    sa.Column('ruler', sa.String(length=64), nullable=True),
    sa.Column('geography_description', sa.String(length=256), nullable=True),
    sa.Column('demographics_description', sa.String(length=256), nullable=True),
    sa.Column('political_description', sa.String(length=256), nullable=True),
    sa.Column('economy_description', sa.String(length=256), nullable=True),
    sa.Column('history_description', sa.String(length=256), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('kingdom_id', sa.Integer(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['kingdom_id'], ['kingdom.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['setting.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_city_kingdom_id'), ['kingdom_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_city_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_city_setting_id'), ['setting_id'], unique=False)

    op.create_table('encounter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('challenge_rating', sa.Float(), nullable=True),
    sa.Column('short_description', sa.String(length=128), nullable=False),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('loot', sa.String(length=512), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('encounter', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_encounter_campaign_id'), ['campaign_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_encounter_owner_id'), ['owner_id'], unique=False)

    op.create_table('point_of_interest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('short_description', sa.String(length=256), nullable=True),
    sa.Column('long_description', sa.String(length=1028), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('kingdom_id', sa.Integer(), nullable=True),
    sa.Column('setting_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['kingdom_id'], ['kingdom.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['setting_id'], ['setting.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('point_of_interest', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_point_of_interest_kingdom_id'), ['kingdom_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_point_of_interest_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_point_of_interest_setting_id'), ['setting_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('point_of_interest', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_point_of_interest_setting_id'))
        batch_op.drop_index(batch_op.f('ix_point_of_interest_owner_id'))
        batch_op.drop_index(batch_op.f('ix_point_of_interest_kingdom_id'))

    op.drop_table('point_of_interest')
    with op.batch_alter_table('encounter', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_encounter_owner_id'))
        batch_op.drop_index(batch_op.f('ix_encounter_campaign_id'))

    op.drop_table('encounter')
    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_city_setting_id'))
        batch_op.drop_index(batch_op.f('ix_city_owner_id'))
        batch_op.drop_index(batch_op.f('ix_city_kingdom_id'))

    op.drop_table('city')
    with op.batch_alter_table('adventure', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_adventure_owner_id'))
        batch_op.drop_index(batch_op.f('ix_adventure_campaign_id'))

    op.drop_table('adventure')
    with op.batch_alter_table('religion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_religion_setting_id'))
        batch_op.drop_index(batch_op.f('ix_religion_owner_id'))

    op.drop_table('religion')
    with op.batch_alter_table('kingdom', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_kingdom_setting_id'))
        batch_op.drop_index(batch_op.f('ix_kingdom_owner_id'))

    op.drop_table('kingdom')
    with op.batch_alter_table('campaign', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_campaign_setting_id'))
        batch_op.drop_index(batch_op.f('ix_campaign_owner_id'))

    op.drop_table('campaign')
    with op.batch_alter_table('setting', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_setting_owner_id'))

    op.drop_table('setting')
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_session_game_master_id'))

    op.drop_table('session')
    op.drop_table('followers')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
