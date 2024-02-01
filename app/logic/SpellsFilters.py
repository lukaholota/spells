class SpellsFilters:
    def __init__(self, form):
        self.form = form
        self.name_filter = form.get('name', '')
        self.classes_filter = form.getlist('classes')
        self.levels_filter = form.getlist('levels')
        self.school_filter = form.get('school', '')
        self.casting_time_filter = form.get('casting_time', '')
        self.ritual_filter = form.get('ritual', '')
        self.concentration_filter = form.get('concentration', '')
        self.sources_filter = form.getlist('sources')

        for i in range(len(self.levels_filter)):
            self.levels_filter.append(self.levels_filter[i] + ' ' + '(ритуал)')
