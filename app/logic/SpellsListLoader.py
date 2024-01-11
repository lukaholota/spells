from app.models import Spell
from app.models import SpellClasses
from app.logic.SpellsFilters import SpellsFilters


class SpellsListLoader:
    def __init__(self, filters: SpellsFilters):
        self.filters = filters
        self.load()

    def load(self):
        query = Spell.query
        query = self.add_filters(query)
        query = query.order_by(Spell.name)
        self.spells = query.all()
        self.reduce_casting_time()

    def add_filters(self, query):
        if self.filters.name_filter:
            query = query.filter(Spell.name.ilike('%' + self.filters.name_filter + '%'))

        if self.filters.class_filter:
            query = query.filter(Spell.classes.any(SpellClasses.class_name == self.filters.class_filter))

        if self.filters.level_filter:
            query = query.filter(Spell.level.ilike('%' + self.filters.level_filter + '%'))

        if self.filters.school_filter:
            query = query.filter(Spell.school.ilike('%' + self.filters.school_filter + '%'))

        if self.filters.casting_time_filter:
            query = query.filter(Spell.casting_time.ilike('%' + self.filters.casting_time_filter + '%'))

        if self.filters.ritual_filter:
            query = query.filter(Spell.has_ritual.ilike('%' + self.filters.ritual_filter + '%'))

        if self.filters.concentration_filter:
            query = query.filter(Spell.has_concentration.ilike('%' + self.filters.concentration_filter + '%'))

        return query

    def reduce_casting_time(self):
        for spell in self.spells:
            if len(spell.casting_time) > 20:
                spell.casting_time = '1 реакція'
