"""add character-character-spells

Revision ID: c31d807c5656
Revises: f2ce7b6aa6bf
Create Date: 2024-01-30 09:57:49.229505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c31d807c5656'
down_revision = 'f2ce7b6aa6bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'character',
        sa.Column('character_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.user_id'))
    )
    op.create_table(
        'character_spells',
        sa.Column('character_spell_id', sa.Integer, primary_key=True),
        sa.Column('character_id', sa.Integer, sa.ForeignKey('character.character_id')),
        sa.Column('spell_id', sa.Integer, sa.ForeignKey('spell.spell_id'))
    )


def downgrade():
    op.drop_table('character_spells')
    op.drop_table('character')
