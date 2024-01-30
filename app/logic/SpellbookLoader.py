from app.models import Spellbook, db


class SpellbookLoader:
    def __init__(self, user):
        self.user = user
        spellbook = self.get_user_spellbook()
        spellbook_spells = spellbook.spells
        self.spells = [spellbook_spell.spell for spellbook_spell in spellbook_spells]

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

    def load(self):
        return self.spells
