from app.models import Spell
from app.models import SpellClasses
from app.logic.SpellsFilters import SpellsFilters
from sqlalchemy import case


class SpellsListLoader:
    def __init__(self, filters: SpellsFilters):
        self.filters = filters
        self.load()

    def load(self):
        query = Spell.query
        query = self.add_filters(query)

        is_cantrip = case((Spell.level == 'замовляння', 0), else_=1)
        query = query.order_by(is_cantrip, Spell.level, Spell.name)
        self.spells = query.all()
        self.reduce_casting_time()

    def add_filters(self, query):
        if self.filters.name_filter:
            query = query.filter(Spell.name.ilike('%' + self.filters.name_filter + '%'))

        if self.filters.classes_filter:
            query = query.filter(Spell.classes.any(SpellClasses.class_name.in_(self.filters.classes_filter)))

        if self.filters.levels_filter:
            query = query.filter(Spell.level.in_(self.filters.levels_filter))

        if self.filters.school_filter:
            query = query.filter(Spell.school == self.filters.school_filter)

        if self.filters.casting_time_filter:
            query = query.filter(Spell.casting_time.ilike('%' + self.filters.casting_time_filter + '%'))

        if self.filters.ritual_filter:
            query = query.filter(Spell.has_ritual == self.filters.ritual_filter)

        if self.filters.concentration_filter:
            query = query.filter(Spell.has_concentration == self.filters.concentration_filter)

        if self.filters.sources_filter:
            query = query.filter(Spell.source.in_(self.filters.sources_filter))

        return query

    def reduce_casting_time(self):
        for spell in self.spells:
            if len(spell.casting_time) > 20:
                spell.casting_time = '1 реакція'

    def make_list_of_dicts(self):
        return [{
            'name': spell.name,
            'level': spell.level,
            'school': spell.school,
            'casting_time': spell.casting_time,
            'has_ritual': spell.has_ritual,
            'has_concentration': spell.has_concentration,
            'source': spell.source,
        } for spell in self.spells]
