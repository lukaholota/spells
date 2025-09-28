from sqlalchemy.orm import selectinload

from app.models import Spell


class SpellRepository:
    def get_spells(self):
        spells = Spell.query.options(
            selectinload(Spell.classes),
            selectinload(Spell.races)
        ).order_by(Spell.name).all()

        return spells
