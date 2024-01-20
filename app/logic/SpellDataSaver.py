from app.models import Spell, SpellClasses, db


class SpellDataSaver:
    def __init__(self, data):
        self.name: str = data.get('spell_name', '')
        self.level: str = data.get('level', '')
        self.school: str = data.get('school', '')
        self.range: str = data.get('range', '')
        self.casting_time: str = data.get('casting_time', '')
        self.duration: str = data.get('duration', '')
        self.components: str = data.get('components', '')
        self.classes: str = data.selected_classes
        self.description: str = data.get('spell_description', '')
        self.has_ritual: str = data.get('has_ritual', '')
        self.has_concentration = 'ні'

        self.process_data()

    def add_new_spell(self):
        spell = Spell(name=self.name,
                      level=self.level,
                      school=self.school,
                      casting_time=self.casting_time,
                      range=self.range,
                      components=self.components,
                      duration=self.duration,
                      description=self.description,
                      has_ritual=self.has_ritual,
                      has_concentration=self.has_concentration
                      )
        db.session.add(spell)
        db.session.flush()
        db.session.refresh(spell)
        for selected_class in self.classes:
            spell_class = SpellClasses(spell_id=spell.spell_id, class_name=selected_class)
            db.session.add(spell_class)
        db.session.commit()

        self.spell_id = spell.spell_id

    def process_data(self):
        self.name = self.name.capitalize().strip()
        self.range = self.range.capitalize().strip()
        self.duration = self.duration.capitalize().strip()

        bracket_index = self.components.find('(')
        components, additional_info = self.components[:bracket_index], self.components[bracket_index:]
        self.components = (components.upper() + additional_info).strip()

        if self.has_ritual == 'true':
            self.level += ' ' + '(ритуал)'
            self.has_ritual = 'так'
        else:
            self.has_ritual = 'ні'
        if 'Концентрація' in self.duration:
            self.has_concentration = 'так'

    def get_spell(self, spell_id):
        self.spell = Spell.query.get_or_404(int(spell_id))
        return self.spell

    def edit_spell(self):
        self.spell.name = self.name
        self.spell.level = self.level
        self.spell.school = self.school
        self.spell.range = self.range
        self.spell.casting_time = self.casting_time
        self.spell.duration = self.duration
        self.spell.components = self.components
        self.spell.description = self.description
        self.spell.has_ritual = self.has_ritual
        self.spell.has_concentration = self.has_concentration

        for spell_class in self.spell.classes:
            SpellClasses.query.filter_by(class_id=spell_class.class_id).delete()

        for selected_class in self.classes:
            spell_class = SpellClasses(spell_id=self.spell.spell_id, class_name=selected_class)
            db.session.add(spell_class)

        db.session.commit()
