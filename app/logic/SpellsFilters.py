class SpellsFilters:
    def __init__(self, form):
        self.form = form
        self.name_filter = form.get('name', '')
        self.class_filter = form.get('class', '')
        self.level_filter = form.get('level', '')
        self.school_filter = form.get('school', '')
        self.casting_time_filter = form.get('casting_time', '')
        self.ritual_filter = form.get('ritual', '')
        self.concentration_filter = form.get('concentration', '')
        self.source_filter = form.get('source', '')
