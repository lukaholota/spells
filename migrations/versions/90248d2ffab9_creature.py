"""creature

Revision ID: 90248d2ffab9
Revises: 9a6f914f71d8
Create Date: 2024-02-15 16:36:25.559497

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '90248d2ffab9'
down_revision = '9a6f914f71d8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'creature',
        sa.Column('creature_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('name_eng', sa.String),
        sa.Column('size', sa.String),
        sa.Column('type', sa.String),
        sa.Column('alignment', sa.String),
        sa.Column('source', sa.String),
        sa.Column('ac', sa.String),
        sa.Column('hp', sa.String),
        sa.Column('speed', sa.String),
        sa.Column('strength', sa.String),
        sa.Column('dexterity', sa.String),
        sa.Column('constitution', sa.String),
        sa.Column('intelligence', sa.String),
        sa.Column('wisdom', sa.String),
        sa.Column('charisma', sa.String),
        sa.Column('skills', sa.String),
        sa.Column('senses', sa.String),
        sa.Column('languages', sa.String),
        sa.Column('challenge', sa.String),
        sa.Column('damage_immunity', sa.String),
        sa.Column('damage_resistance', sa.String),
        sa.Column('condition_immunity', sa.String),
        sa.Column('saving_throws', sa.String),
        sa.Column('special_abilities', sa.String),
        sa.Column('actions', sa.String),
        sa.Column('bonus_actions', sa.String),
        sa.Column('reactions', sa.String),
        sa.Column('legendary_actions', sa.String)
    )


def downgrade():
    op.drop_table('creature')
