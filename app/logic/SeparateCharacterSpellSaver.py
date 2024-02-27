from app.models import CharacterSpells, db


class SeparateCharacterSpellSaver:
    def __init__(self, character_id, spell_id):
        self.character_id = character_id
        self.spell_id = spell_id

    def save(self):
        if not CharacterSpells.query.filter_by(character_id=self.character_id, spell_id=self.spell_id).first():
            spell = CharacterSpells(character_id=self.character_id, spell_id=self.spell_id)
            db.session.add(spell)
            db.session.commit()
