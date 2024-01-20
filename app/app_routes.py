from app.app import app
from flask import render_template, request
from app.logic.SpellLoader import SpellLoader
from app.logic.SpellsListLoader import SpellsListLoader
from app.logic.SpellsFilters import SpellsFilters
from app.logic.SpellsForm import SpellsForm
from app.logic.SpellDataSaver import SpellDataSaver


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/spell/<spell_id>')
def load_spell(spell_id):
    spell_loader = SpellLoader(spell_id)
    return render_template('spell.html',
                           spell_name=spell_loader.spell_name,
                           school=spell_loader.school,
                           level=spell_loader.level,
                           casting_time=spell_loader.casting_time,
                           range=spell_loader.range,
                           components=spell_loader.components,
                           duration=spell_loader.duration,
                           spell_description=spell_loader.description,
                           spell_classes=spell_loader.classes,
                           )


@app.route('/spells', methods=['GET', 'POST'])
def load_spells_list():
    spells_filters = SpellsFilters(request.form)
    spells_list_loader = SpellsListLoader(spells_filters)
    spells_form = SpellsForm()

    return render_template('spells.html',
                           spells=spells_list_loader.spells,
                           form=spells_form,
                           filters=spells_filters
                           )


@app.route('/add-spell',  methods=['GET', 'POST'])
def add_spell():
    results = request.form
    results.selected_classes = results.getlist('classes')
    if request.method == 'POST':
        spell_data_saver = SpellDataSaver(results)
        spell_data_saver.add_new_spell()

    form = SpellsForm()
    return render_template('add-spell.html',
                           results=results,
                           form=form
                           )
