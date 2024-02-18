"""maky_columns

Revision ID: 1108a872e7fd
Revises: cba929f3e763
Create Date: 2024-02-15 17:16:19.612980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1108a872e7fd'
down_revision = 'cba929f3e763'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creature', sa.Column('description', sa.String))
    op.add_column('creature', sa.Column('lair_actions', sa.String))
    op.add_column('creature', sa.Column('lair_info', sa.String))
    op.add_column('creature', sa.Column('region_effects', sa.String))


def downgrade():
    op.drop_column('creature', 'description')
    op.drop_column('creature', 'lair_action')
    op.drop_column('creature', 'lair_info')
    op.drop_column('creature', 'region_effects')
