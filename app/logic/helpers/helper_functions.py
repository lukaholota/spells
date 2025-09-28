def get_spells_by_level(spells):
    spells_by_level = {
        'замовляння': [],
        '1 рівень': [],
        '2 рівень': [],
        '3 рівень': [],
        '4 рівень': [],
        '5 рівень': [],
        '6 рівень': [],
        '7 рівень': [],
        '8 рівень': [],
        '9 рівень': [],
    }

    for spell in spells:
        spells_by_level[spell.level.strip(' (ритуал)')].append(spell)

    return spells_by_level