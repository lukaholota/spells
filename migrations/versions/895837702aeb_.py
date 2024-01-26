"""empty message

Revision ID: 895837702aeb
Revises: eb02364120b0
Create Date: 2024-01-26 18:23:25.114069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895837702aeb'
down_revision = 'eb02364120b0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('spell_races',
                    sa.Column('spell_id', sa.Integer, sa.ForeignKey('spell.spell_id')),
                    sa.Column('race_id', sa.Integer, primary_key=True),
                    sa.Column('race_name', sa.String)
                    )


def downgrade():
    op.drop_table('spell_races')
