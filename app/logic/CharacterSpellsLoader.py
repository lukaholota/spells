from app.models import Character, CharacterSpells, Spell


class CharacterSpellsLoader:
    def __init__(self, character_id):
        self.character = Character.query.get(character_id)
        self.spells = [character_spell.spell for character_spell in self.character.spells]

    def load(self):
        return self.spells
