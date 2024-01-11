"""add_concentration_and_ritual_fields_to_spell2

Revision ID: c373872e048a
Revises: b70abbb00e8f
Create Date: 2024-01-09 10:17:20.167602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c373872e048a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "spell",
        sa.Column('has_ritual', sa.String)
    )
    op.add_column(
        "spell",
        sa.Column('has_concentration', sa.String)
    )


def downgrade():
    op.drop_column('spell', 'has_ritual')
    op.drop_column('spell', 'has_concentration')
