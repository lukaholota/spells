"""add-source

Revision ID: eb02364120b0
Revises: 6958494a77cf
Create Date: 2024-01-21 10:53:55.813778

"""
from alembic import op
import sqlalchemy as sa
from app.models import Spell

# revision identifiers, used by Alembic.
revision = 'eb02364120b0'
down_revision = '6958494a77cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('spell', sa.Column('source', sa.String, nullable=False, server_default='Книга гравця'))



def downgrade():
    op.drop_column('spell', 'source')
