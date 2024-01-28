"""user

Revision ID: c5f7246eb51a
Revises: 895837702aeb
Create Date: 2024-01-27 09:30:32.979639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5f7246eb51a'
down_revision = '895837702aeb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String),
        sa.Column('password', sa.String),
    )


def downgrade():
    op.drop_table('user')
