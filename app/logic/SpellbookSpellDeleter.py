from app.models import SpellbookSpells, db


class SpellbookSpellDeleter:
    def __init__(self, spell_id):
        self.spell_id = spell_id

    def delete(self):
        SpellbookSpells.query.filter_by(spell_id=self.spell_id).delete()
        db.session.commit()
