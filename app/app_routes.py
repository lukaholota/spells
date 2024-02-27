from app.app import app, auth
from app.logic.CreatureLoader import CreatureLoader
from flask import render_template, request, redirect, flash, abort, send_file, jsonify
from flask_login import logout_user, login_required, current_user
from app.logic.SpellLoader import SpellLoader
from app.logic.SpellsListLoader import SpellsListLoader
from app.logic.SpellsFilters import SpellsFilters
from app.logic.SpellsForm import SpellsForm
from app.logic.SpellDataSaver import SpellDataSaver
from app.logic.Authenticator import Authenticator
from app.logic.SpellbookSaver import SpellbookSaver
from app.logic.SpellbookLoader import SpellbookLoader
from app.logic.SpellbookSpellDeleter import SpellbookSpellDeleter
from app.logic.CharacterCreator import CharacterCreator
from app.logic.CharacterSpellsSaver import CharacterSpellsSaver
from app.logic.CharacterDeleter import CharacterDeleter
from app.logic.CharacterSpellsLoader import CharacterSpellsLoader
from app.logic.CharacterSpellDeleter import CharacterSpellDeleter
from app.logic.SpelllistCreator import SpelllistCreator
from app.logic.CreaturesForm import CreaturesForm
from app.logic.CreatureDataSaver import CreatureDataSaver
from app.logic.EmptyUserHandler import EmptyUserHandler


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


@app.route('/spells', methods=['GET'])
def load_spells_list():
    empty_user_handler = EmptyUserHandler(current_user)
    if empty_user_handler.check_if_empty():
        return empty_user_handler.handle_empty()

    spells_filters = SpellsFilters(request.form)
    spells_list_loader = SpellsListLoader(spells_filters)
    spells_form = SpellsForm()

    return render_template('spells.html',
                           spells=spells_list_loader.spells,
                           form=spells_form,
                           filters=spells_filters,
                           )


@app.route('/spells', methods=['POST'])
def apply_filters_to_spelllist():
    spells_filters = SpellsFilters(request.form)
    spells_list_loader = SpellsListLoader(spells_filters)

    return jsonify(spells_list_loader.make_list_of_dicts())


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
    if not authenticator.validate():
        flash('Логін не може бути порожнім')
        return redirect('/sign-up')
    if authenticator.check_if_exists():
        flash('Логін уже зайнято')
        return redirect('/sign-up')

    authenticator.add_new_user()

    return redirect('/spells')


@app.route('/log-in')
def log_in():
    return render_template('log-in.html')


@app.route('/log-in', methods=['POST'])
def log_in_post():
    data = request.form
    authenticator = Authenticator(data)
    if authenticator.log_in():
        return redirect('/spells')

    flash('Перевірте дані та спробуйте ще раз')
    return redirect('/log-in')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/spells')


@app.route('/sorry-registration')
def sorry_registration():
    return render_template('sorry-registration.html')


@app.route('/sorry-registration', methods=['POST'])
def sorry_registration_post():
    data = request.form
    authenticator = Authenticator(data)
    if not authenticator.validate():
        flash('Логін не може бути порожнім')
        return redirect('/sorry-registration')
    if authenticator.check_if_exists():
        flash('Логін уже зайнято')
        return redirect('/sorry-registration')

    new_user = authenticator.add_new_user()

    empty_user_handler = EmptyUserHandler(new_user)
    empty_user_handler.transfer_data()

    return redirect('/spells')


@app.route('/spellbook')
@login_required
def spellbook():
    spellbook_loader = SpellbookLoader(current_user)
    spells = spellbook_loader.load()

    character_list = current_user.characters
    return render_template('spellbook.html', spells=spells, character_list=character_list)


@app.route('/add-to-spellbook', methods=['POST'])
def add_to_spellbook():
    if current_user.is_authenticated == False:
        abort(403)
    spell_id = request.get_json()['id']
    spellbook_saver = SpellbookSaver(current_user)
    spellbook_saver.add_spell_to_spellbook(spell_id)

    return ''


@app.route('/hybrid-registration', methods=['POST'])
def hybrid_registration():
    authenticator = Authenticator(request.form)

    if not authenticator.validate():
        return {'result': False, 'message': 'Логін не може бути порожнім'}

    if authenticator.check_if_exists():
        if authenticator.log_in():
            return {'result': True, 'message': 'Ви успішно ввійшли'}
        else:
            return {'result': False, 'message': 'Дані введено невірно'}

    else:
        authenticator.add_new_user()
        return {'result': True, 'message': 'Нового користувача успішно додано'}


@app.route('/delete-spellbook-spell', methods=['POST'])
@login_required
def delete_spellbook_spell():
    spell_id = request.form.get('spell_id', '')
    spellbook_spell_deleter = SpellbookSpellDeleter(spell_id)
    spellbook_spell_deleter.delete()

    return redirect('/spellbook')


@app.route('/create-character/<source>')
@login_required
def create_character(source):
    return render_template('create-character.html', source=source)


@app.route('/create-character', methods=['POST'])
@login_required
def create_character_post():
    data = request.form
    character_creator = CharacterCreator(data, current_user)
    if not character_creator.create():
        flash(character_creator.message)
        return redirect(f'create-character/{data.get("source", "characters")}')
    return redirect(f'/{data.get("source", "characters")}')


@app.route('/add-spells-to-character', methods=['POST'])
@login_required
def add_spells_to_character():
    character_spells_saver = CharacterSpellsSaver(request.form, current_user)
    if character_spells_saver.save():
        character_spells_saver.make_spellbook_empty()
        return redirect(f'/characters/{character_spells_saver.character.character_id}')
    else:
        flash('Щось пішло шкереберть')
    return render_template('spellbook.html', character_id=character_spells_saver.character.character_id)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/characters')
@login_required
def characters():
    character_list = current_user.characters
    return render_template('characters.html', character_list=character_list)


@app.route('/delete-character', methods=['POST'])
@login_required
def delete_character():
    character_id = request.form.get('character_id', '')
    character_deleter = CharacterDeleter(character_id)
    character_deleter.delete()

    return redirect('/characters')


@app.route('/characters/<character_id>')
@login_required
def character(character_id):
    if not int(character_id) in [character.character_id for character in current_user.characters]:
        abort(403)
    character_spells_loader = CharacterSpellsLoader(character_id)
    spells = character_spells_loader.load()

    return render_template(
        'character.html',
        spells=spells,
        character_name=character_spells_loader.character.name,
        character_id=character_spells_loader.character.character_id
    )


@app.route('/delete-character-spell', methods=['POST'])
@login_required
def delete_character_spell():
    data = request.form
    spell_id = data.get('spell_id', '')
    character_spell_deleter = CharacterSpellDeleter(spell_id)
    character_spell_deleter.delete()

    return redirect(f'/characters/{data.get("source")}')


@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap_v2.xml')


@app.route('/create-spelllist-from-character', methods=['POST'])
@login_required
def create_spelllist_from_character():
    spelllist_creator = SpelllistCreator()

    spelllist_creator.get_spells_from_character(request.form.get('character_id', ''))
    buffer = spelllist_creator.create_spelllist()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf')


@app.route('/create-spelllist-from-spellbook', methods=['POST'])
@login_required
def create_spelllist_from_spellbook():
    spelllist_creator = SpelllistCreator()
    spelllist_creator.get_spells_from_spellbook(current_user.spellbook.spellbook_id)
    buffer = spelllist_creator.create_spelllist()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf')


@app.route('/create-spelllist-by-ids', methods=['POST'])
def create_spelllist_by_ids():
    spelllist_creator = SpelllistCreator()
    spelllist_creator.get_spells_by_ids(request.form.getlist('selected_spells'))
    buffer = spelllist_creator.create_spelllist()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf')


@app.route('/add-creature',  methods=['GET', 'POST'])
@auth.login_required
def add_creature():
    results = request.form
    form = CreaturesForm()
    if request.method == 'POST':
        creature_data_saver = CreatureDataSaver()
        creature_data_saver.custom_init(results, form)
        creature_data_saver.add_new_creature()
        return redirect(f'/edit-creature/{creature_data_saver.creature_id}')

    return render_template('add-creature.html',
                           results=results,
                           form=form
                           )


@app.route('/edit-creature/<id>',  methods=['GET', 'POST'])
@auth.login_required
def edit_creature(id):
    results = request.form
    form = CreaturesForm()
    creature_data_saver = CreatureDataSaver()
    creature = creature_data_saver.get_creature(id)
    if request.method == 'POST':
        creature_data_saver.custom_init(results, form)
        creature_data_saver.edit_creature()

    return render_template(
        'edit-creature.html',
        creature=creature,
        form=form
        )


@app.route('/creature/<id>')
def creature(id):
    creature_loader = CreatureLoader(id)

    return render_template(
        'creature.html',
        creature=creature_loader.creature
    )


@app.route('/get-spellbook-spells')
def get_spellbook_spells():
    spellbook_spells = []
    if current_user.is_authenticated:
        spellbook_spells = [spell.spell_id for spell in current_user.spellbook.spells]

    return jsonify(spellbook_spells)


@app.route('/get-user-info')
def get_user_info():
    return jsonify({'is_authenticated': current_user.is_authenticated})
