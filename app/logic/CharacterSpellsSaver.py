from app.models import CharacterSpells, Character, db, SpellbookSpells


class CharacterSpellsSaver:
    def __init__(self, data, user):
        self.character = Character.query.filter_by(character_id=data.get('character_id', '')).first()
        self.spellbook = user.spellbook
        self.spells = self.spellbook.spells

    def save(self):
        if self.spells:
            spells_to_add = []
            character_spell_ids = set(spell.spell_id for spell in self.character.spells)
            for spell in self.spells:
                if spell.spell_id not in character_spell_ids:
                    character_spell = CharacterSpells(spell_id=spell.spell_id, character_id=self.character.character_id)
                    spells_to_add.append(character_spell)
            if spells_to_add:
                db.session.add_all(spells_to_add)
            return True
        else:
            return False

    def make_spellbook_empty(self):
        SpellbookSpells.query.filter_by(spellbook_id=self.spellbook.spellbook_id).delete()
        db.session.commit()


