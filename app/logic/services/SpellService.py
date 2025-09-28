from app.repository.SpellRepository import SpellRepository


class SpellService:
    def __init__(self):
        self.spell_repository = SpellRepository()

    def get_spells(self):
        return self.spell_repository.get_spells()

