from app.models import Spell, SpellClasses


class SpellLoader:
    def __init__(self, spell_id):
        self.spell_id = spell_id
        self.load()

    def load(self):
        spell = Spell.query.get_or_404(int(self.spell_id))
        self.spell_name = spell.name
        self.level = spell.level
        self.school = spell.school
        self.casting_time = spell.casting_time
        self.range = spell.range
        self.components = spell.components
        self.duration = spell.duration
        self.description = spell.description
        self.classes = self.get_classes_names(spell)
        self.source = spell.source
        self.races = self.get_races_names(spell)

    def get_classes_names(self, spell):
        classes = spell.classes
        classes_names = ''

        for i in range(len(classes)):
            class_name = classes[i]
            classes_names += class_name.class_name
            if i != len(classes) - 1:
                classes_names += ', '

        return classes_names

    def get_races_names(self, spell):
        races = spell.races
        races_names = ''

        for i in range(len(races)):
            race_name = races[i]
            races_names += race_name.race_name
            if i != len(races) - 1:
                races_names += ', '

        return races_names
