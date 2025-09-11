class SpellsFilters:
    def __init__(self, params):
        self.params = params
        self.name_filter = params.get('name', '').strip()
        self.classes_filter = params.getlist('classes')
        self.levels_filter = params.getlist('levels')
        self.school_filter = params.get('school', '')
        self.casting_time_filter = params.get('casting_time', '')
        self.ritual_filter = params.get('ritual', '')
        self.concentration_filter = params.get('concentration', '')
        self.sources_filter = params.getlist('sources')

        for i in range(len(self.levels_filter)):
            self.levels_filter.append(self.levels_filter[i] + ' ' + '(ритуал)')
