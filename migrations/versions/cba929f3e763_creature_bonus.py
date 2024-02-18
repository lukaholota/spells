"""creature_bonus

Revision ID: cba929f3e763
Revises: 90248d2ffab9
Create Date: 2024-02-15 16:54:37.601337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba929f3e763'
down_revision = '90248d2ffab9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('creature', sa.Column('proficiency_bonus', sa.String))


def downgrade():
    op.drop_column('creature', 'proficiency_bonus')
