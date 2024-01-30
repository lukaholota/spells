from app.models import CharacterSpells, db


class CharacterSpellDeleter:
    def __init__(self, spell_id):
        self.spell_id = spell_id

    def delete(self):
        CharacterSpells.query.filter_by(spell_id=self.spell_id).delete()
        db.session.commit()
