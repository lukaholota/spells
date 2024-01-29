"""add-user-column-to-spellbook

Revision ID: f2ce7b6aa6bf
Revises: 5926f9663996
Create Date: 2024-01-28 11:20:30.904072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2ce7b6aa6bf'
down_revision = '5926f9663996'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('spellbook', sa.Column('user_id', sa.Integer, sa.ForeignKey('user.user_id')))
    op.create_foreign_key('fk_user_id', 'spellbook', 'user', ['user_id'], ['user_id'])


def downgrade():
    op.drop_constraint('fk_user_id', 'spellbook')
    op.drop_column('spellbook', 'user_id')
