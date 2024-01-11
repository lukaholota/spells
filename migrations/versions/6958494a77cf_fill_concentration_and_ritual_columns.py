"""fill_concentration_and_ritual_columns

Revision ID: 6958494a77cf
Revises: c373872e048a
Create Date: 2024-01-10 09:47:41.334373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session as ormSession
from app.models import Spell


# revision identifiers, used by Alembic.
revision = '6958494a77cf'
down_revision = 'c373872e048a'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    session = ormSession(connection)
    session.execute(
        sa.update(Spell).values({
            'has_concentration': sa.case(
                (
                    (Spell.duration.match('Концентрація%')),
                    'так'
                ), else_='ні'
            ),
            'has_ritual': sa.case(
                (
                    (Spell.level.match('%ритуал%')),
                    'так'
                ), else_='ні'
            )
        })
    )
    session.commit()
    session.close()


def downgrade():
    connection = op.get_bind()
    session = ormSession(connection)
    session.execute(
        sa.update(Spell).values({'has_ritual': '', 'has_concentration': ''})
    )
    session.commit()
    session.close()

