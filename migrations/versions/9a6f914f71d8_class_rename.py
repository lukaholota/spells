"""class rename

Revision ID: 9a6f914f71d8
Revises: c31d807c5656
Create Date: 2024-02-02 10:54:12.678625

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session as ormSession
from app.models import SpellClasses


# revision identifiers, used by Alembic.
revision = '9a6f914f71d8'
down_revision = 'c31d807c5656'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    session = ormSession(connection)
    try:
        session.execute(
            sa.update(SpellClasses).values({
                'class_name': 'чародій'
            }).where(SpellClasses.class_name == 'заклинач')
        )
        session.execute(
            sa.update(SpellClasses).values({
                'class_name': 'чорнокнижник'
            }).where(SpellClasses.class_name == 'чаклун')
        )
        session.commit()

        check = session.query(SpellClasses).get('2505')
        if check.class_name != 'паладин':
            raise Exception
    except:
        session.rollback()

    session.close()


def downgrade():
    connection = op.get_bind()
    session = ormSession(connection)
    try:
        session.execute(
            sa.update(SpellClasses).values({
                'class_name': 'заклинач'
            }).where(SpellClasses.class_name == 'чародій')
        )
        session.execute(
            sa.update(SpellClasses).values({
                'class_name': 'чаклун'
            }).where(SpellClasses.class_name == 'чорнокнижник')
        )
        session.commit()
        check = session.query(SpellClasses).get('2505')
        if check.class_name != 'паладин':
            raise Exception
    except:
        session.rollback()

    session.close()
