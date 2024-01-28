"""spellbook-spellbookspells

Revision ID: 5926f9663996
Revises: c5f7246eb51a
Create Date: 2024-01-28 11:07:16.303752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5926f9663996'
down_revision = 'c5f7246eb51a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('spellbook',
                    sa.Column('spellbook_id', sa.Integer, primary_key=True))
    op.create_table('spellbook_spells',
                    sa.Column('spellbook_spell_id', sa.Integer, primary_key=True),
                    sa.Column('spell_id', sa.Integer, sa.ForeignKey('spell.spell_id')),
                    sa.Column('spellbook_id', sa.Integer, sa.ForeignKey('spellbook.spellbook_id'))
                    )


def downgrade():
    op.drop_table('spellbook_spells')
    op.drop_table('spellbook')
