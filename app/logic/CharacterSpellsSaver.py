from app.models import CharacterSpells, Character, db, SpellbookSpells


class CharacterSpellsSaver:
    def __init__(self, data, user):
        self.character = Character.query.filter_by(character_id=data.get('character_id', '')).first()
        self.spellbook = user.spellbook
        self.spells = self.spellbook.spells

    def save(self):
        if self.spells:
            for spell in self.spells:
                if not CharacterSpells.query.filter_by(spell_id=spell.spell_id, character_id=self.character.character_id).first():
                    character_spell = CharacterSpells(spell_id=spell.spell_id, character_id=self.character.character_id)
                    db.session.add(character_spell)
            db.session.commit()
            return True
        else:
            return False

    def make_spellbook_empty(self):
        SpellbookSpells.query.filter_by(spellbook_id=self.spellbook.spellbook_id).delete()
        db.session.commit()


