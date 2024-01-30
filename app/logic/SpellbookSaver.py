from app.models import Spellbook, SpellbookSpells, User, db


class SpellbookSaver:
    def __init__(self, spell_ids, user):
        self.spell_ids = spell_ids
        self.user = user
        self.spellbook = self.get_user_spellbook()

    def get_user_spellbook(self):
        if self.user.spellbook:
            return self.user.spellbook

        spellbook = self.create_spellbook_for_user()
        return spellbook

    def create_spellbook_for_user(self):
        spellbook = Spellbook(user_id=self.user.user_id)
        db.session.add(spellbook)
        db.session.commit()
        db.session.flush()
        db.session.refresh(spellbook)
        return spellbook

    def add_spells_to_spellbook(self):
        for spell_id in self.spell_ids:
            if not SpellbookSpells.query.filter_by(spellbook_id=self.spellbook.spellbook_id, spell_id=spell_id).first():
                spellbook_spell = SpellbookSpells(spellbook_id=self.spellbook.spellbook_id, spell_id=int(spell_id))
                db.session.add(spellbook_spell)
        db.session.commit()

