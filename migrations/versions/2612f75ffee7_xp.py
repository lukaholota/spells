"""xp

Revision ID: 2612f75ffee7
Revises: 1108a872e7fd
Create Date: 2024-02-17 22:38:52.241419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2612f75ffee7'
down_revision = '1108a872e7fd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creature', sa.Column('xp', sa.String))


def downgrade():
    op.drop_column('creature', 'xp')
