from app.models import Spellbook, SpellbookSpells, User, db


class SpellbookSaver:
    def __init__(self, spells, user):
        self.spells = spells
        self.user = User.query.get(user.user_id)
        self.spellbook = self.get_user_spellbook()

    def get_user_spellbook(self):
        if self.user.spellbook is not None:
            return self.user.spellbook

        spellbook = self.create_spellbook_for_user()
        return spellbook

    def create_spellbook_for_user(self):
        spellbook = Spellbook(self.user.user_id)
        db.session.add(spellbook)
        db.session.commit()
        db.refresh(spellbook)
        return spellbook

    def add_spells_to_spellbook(self):
        for spell in self.spells:
            if not SpellbookSpells.query.get(spell.spell_id):
                spellbook_spell = SpellbookSpells(spellbook_id=self.spellbook.spellbook_id, spell_id=spell.spell_id)
                db.session.add(spellbook_spell)
        db.session.commit()

