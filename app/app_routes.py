from app.app import app, auth
from flask import render_template, request, redirect, flash, abort
from flask_login import logout_user, login_required, current_user, login_user
from app.logic.SpellLoader import SpellLoader
from app.logic.SpellsListLoader import SpellsListLoader
from app.logic.SpellsFilters import SpellsFilters
from app.logic.SpellsForm import SpellsForm
from app.logic.SpellDataSaver import SpellDataSaver
from app.logic.Authenticator import Authenticator
from app.logic.SpellbookSaver import SpellbookSaver
from app.logic.SpellbookLoader import SpellbookLoader


@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'ASMDAMD!*(#@EH!HJBf':
        return username


@app.route('/')
def home():
    return redirect('spells')


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
                           source=spell_loader.source,
                           spell_races=spell_loader.races
                           )


@app.route('/spells', methods=['GET', 'POST'])
def load_spells_list():
    spells_filters = SpellsFilters(request.form)
    spells_list_loader = SpellsListLoader(spells_filters)
    spells_form = SpellsForm()

    return render_template('spells.html',
                           spells=spells_list_loader.spells,
                           form=spells_form,
                           filters=spells_filters,
                           current_user=current_user
                           )


@app.route('/add-spell',  methods=['GET', 'POST'])
@auth.login_required
def add_spell():
    results = request.form
    results.selected_classes = results.getlist('classes')
    results.selected_races = results.getlist('races')
    form = SpellsForm()
    if request.method == 'POST':
        spell_data_saver = SpellDataSaver(results)
        spell_data_saver.add_new_spell()
        return redirect(f'edit-spell/{spell_data_saver.spell_id}')

    return render_template('add-spell.html',
                           results=results,
                           form=form
                           )


@app.route('/edit-spell/<spell_id>',  methods=['GET', 'POST'])
@auth.login_required
def edit_spell(spell_id):
    results = request.form
    results.selected_classes = results.getlist('classes')
    results.selected_races = results.getlist('races')
    spell_data_saver = SpellDataSaver(results)
    spell = spell_data_saver.get_spell(spell_id)
    if request.method == 'POST':
        spell_data_saver.edit_spell()

    form = SpellsForm()
    classes_list = [spell_class.class_name for spell_class in spell.classes]
    races_list = [spell_race.race_name for spell_race in spell.races]
    spell.classes_list = classes_list
    spell.races_list = races_list

    return render_template('edit-spell.html',
                           spell=spell,
                           form=form
                           )


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')


@app.route('/sign-up', methods=['POST'])
def sign_up_post():
    data = request.form
    authenticator = Authenticator(data)
    if authenticator.check_if_exists():
        flash('Логін уже зайнято')
        return redirect('/sign-up')

    authenticator.add_new_user()

    return redirect('/spells')


@app.route('/log-in')
def log_in():
    return render_template('log-in.html')


@app.route('/sign-in', methods=['POST'])
def log_in_post():
    data = request.form
    authenticator = Authenticator(data)
    if authenticator.log_in():
        return redirect('/spells')

    flash('Перевірте дані та спробуйте ще раз')
    return redirect('log-in')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/spells')


@app.route('/spellbook')
@login_required
def spellbook():
    spellbook_loader = SpellbookLoader(current_user)
    spells = spellbook_loader.load()

    return render_template('spellbook.html', spells=spells)


@app.route('/add-to-spellbook', methods=['POST'])
def add_to_spellbook():
    if current_user.is_authenticated == False:
        abort(403)
    spells = request.form.getlist('selected_spells')
    spellbook_saver = SpellbookSaver(spells, current_user)
    spellbook_saver.add_spells_to_spellbook()

    return ''


@app.route('/hybrid-registration', methods=['POST'])
def hybrid_registration():
    authenticator = Authenticator(request.form)

    if authenticator.check_if_exists():
        if authenticator.log_in():
            return {'result': True, 'message': 'Ви успішно ввійшли'}
        else:
            return {'result': False, 'message': 'Дані введено невірно'}

    else:
        authenticator.add_new_user()
        return {'result': True, 'message': 'Нового користувача успішно додано'}
