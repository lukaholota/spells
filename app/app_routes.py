from flask import render_template, request, redirect, abort, send_file, \
    jsonify
from flask_login import logout_user, login_required, current_user

from app.app import app, auth, cache
from app.db import db
from app.logic.Authenticator import Authenticator
from app.logic.CharacterCreator import CharacterCreator
from app.logic.CharacterDeleter import CharacterDeleter
from app.logic.CharacterSpellDeleter import CharacterSpellDeleter
from app.logic.CharacterSpellsLoader import CharacterSpellsLoader
from app.logic.CharacterSpellsSaver import CharacterSpellsSaver
from app.logic.CreatureDataSaver import CreatureDataSaver
from app.logic.CreatureLoader import CreatureLoader
from app.logic.CreaturesForm import CreaturesForm
from app.logic.SpellDataSaver import SpellDataSaver
from app.logic.SpellPrinter import SpellPrinter
from app.logic.SpellbookLoader import SpellbookLoader
from app.logic.SpellbookSaver import SpellbookSaver
from app.logic.SpellbookSpellDeleter import SpellbookSpellDeleter
from app.logic.SpellsForm import SpellsForm
from app.logic.SpellsFormCreate import SpellsFormCreate
from app.logic.helpers.helper_functions import get_spells_by_level
from app.logic.services.SpellService import SpellService
from app.schemas.spells import spells_schema


@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'ASMDAMD!*(#@EH!HJBf':
        return username


@app.route('/')
def home():
    return redirect('spells')


@app.route('/spell/<spell_id>')
def load_spell(spell_id):
    return redirect(f'/spells?selectedSpellId={spell_id}')


@app.route('/spells', methods=['GET'])
def load_spells():
    spells = cache.get('spells')
    if not spells:
        service = SpellService()
        spells = service.get_spells()
        cache.set('spells', spells, timeout=86400)

    spells_by_level = get_spells_by_level(spells)
    level_by_id = {s.spell_id: lvl for lvl, lst in spells_by_level.items() for
                   s in lst}

    spells_form = SpellsForm()
    return render_template('spells-v3.html',
                           spells_by_level=spells_by_level,
                           form=spells_form,
                           spells=spells_schema.dump(spells),
                           level_by_id=level_by_id,
                           )


@app.route('/add-spell', methods=['GET', 'POST'])
@auth.login_required
def add_spell():
    results = request.form
    results.selected_classes = results.getlist('classes')
    results.selected_races = results.getlist('races')
    form = SpellsFormCreate()
    if request.method == 'POST':
        spell_data_saver = SpellDataSaver(results)
        spell_data_saver.add_new_spell()
        cache.delete('spells_by_level')
        return redirect(f'edit-spell/{spell_data_saver.spell_id}')

    return render_template('add-spell.html',
                           results=results,
                           form=form
                           )


@app.route('/edit-spell/<spell_id>', methods=['GET', 'POST'])
@auth.login_required
def edit_spell(spell_id):
    results = request.form
    results.selected_classes = results.getlist('classes')
    results.selected_races = results.getlist('races')
    spell_data_saver = SpellDataSaver(results)
    spell = spell_data_saver.get_spell(spell_id)
    if request.method == 'POST':
        spell_data_saver.edit_spell()

        cache.delete('spells_by_level')

    form = SpellsFormCreate()
    classes_list = [spell_class.class_name for spell_class in spell.classes]
    races_list = [spell_race.race_name for spell_race in spell.races]
    spell.classes_list = classes_list
    spell.races_list = races_list

    return render_template('edit-spell.html',
                           spell=spell,
                           form=form
                           )


@app.route('/sign-in')
def sign_in():
    next = request.args.get("next", "")

    if '/spellbook' not in next and '/logout' not in next and '/characters' not in next:
        next = ''

    return redirect(f'spells?sign-in=true&next={next}')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return {'success': True}


@app.route('/spellbook')
@login_required
def spellbook():
    spellbook_loader = SpellbookLoader(current_user)
    spells = spellbook_loader.load()

    character_list = [
        {'character_id': character.character_id, 'name': character.name} for
        character in current_user.characters]
    spells_by_level = get_spells_by_level(spells)
    level_by_id = {s.spell_id: lvl for lvl, lst in spells_by_level.items() for
                   s in lst}

    spells_form = SpellsForm()
    return render_template('spellbook-v2.html',
                           spells=spells_schema.dump(spells),
                           character_list=character_list,
                           spells_by_level=spells_by_level,
                           level_by_id=level_by_id,
                           form=spells_form
                           )


@app.route('/add-to-spellbook', methods=['POST'])
def add_to_spellbook():
    if current_user.is_authenticated == False:
        abort(403)
    spell_id = int(request.get_json().get('spell_id'))
    spellbook_saver = SpellbookSaver(current_user)
    spellbook_saver.add_spell_to_spellbook(spell_id)

    cache.delete(f'spellbook_spell_ids:{current_user.user_id}')

    return {'result': True}


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
    spell_id = int(request.get_json().get('spell_id'))
    spellbook_spell_deleter = SpellbookSpellDeleter(spell_id)
    spellbook_spell_deleter.delete()

    cache.delete(f'spellbook_spell_ids:{current_user.user_id}')

    return {'result': True}


@app.route('/create-character', methods=['POST'])
@login_required
def create_character_post():
    data = request.form
    character_creator = CharacterCreator(data, current_user)

    if not character_creator.validate():
        return {'result': False, 'message': character_creator.message}
    character = character_creator.create()
    return {'result': True, 'message': '',
            'character': {'character_id': character.character_id,
                          'name': character.name}}


@app.route('/add-spells-to-character', methods=['POST'])
@login_required
def add_spells_to_character():
    character_spells_saver = CharacterSpellsSaver(request.get_json(),
                                                  current_user)
    if character_spells_saver.save():
        character_spells_saver.make_spellbook_empty()
        cache.delete(f'spellbook_spell_ids:{current_user.user_id}')
        return {'result': True,
                'redirect_url': f'/characters/{character_spells_saver.character.character_id}'}
    else:
        db.session.rollback()
        return {'result': False}


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/delete-character', methods=['POST'])
@login_required
def delete_character():
    character_id = request.get_json().get('character_id', '')
    character_deleter = CharacterDeleter(character_id)
    try:
        character_deleter.delete()
        return {'result': True}
    except Exception as e:
        print(e)
        db.session.rollback()
        return {'result': False}


@app.route('/characters/<character_id>')
@login_required
def character(character_id):
    if int(character_id) not in [character.character_id for character in
                                 current_user.characters]:
        return redirect('/spells')
    character_spells_loader = CharacterSpellsLoader(character_id)
    spells = character_spells_loader.load()

    character_list = [
        {'character_id': character.character_id, 'name': character.name} for
        character in current_user.characters if character.character_id != int(character_id)]
    spells_by_level = get_spells_by_level(spells)
    level_by_id = {s.spell_id: lvl for lvl, lst in spells_by_level.items() for
                   s in lst}

    spells_form = SpellsForm()

    return render_template(
        'character-v2.html',
        spells=spells_schema.dump(spells),
        character_list=character_list,
        level_by_id=level_by_id,
        spells_by_level=spells_by_level,
        form=spells_form,
        character_name=character_spells_loader.character.name,
        character_id=character_spells_loader.character.character_id
    )


@app.route('/delete-character-spell', methods=['POST'])
@login_required
def delete_character_spell():
    spell_id = request.get_json().get('spell_id', '')
    character_spell_deleter = CharacterSpellDeleter(spell_id)
    character_spell_deleter.delete()

    return {'result': True}


@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap_v3.xml')

@app.route('/robots.txt')
def robots():
    return send_file('robots.txt')


@app.route('/print-spells', methods=['POST'])
def print_spells():
    selected_spells = request.get_json().get('selected_spells', [])

    spell_printer = SpellPrinter()
    spell_printer.get_spells_by_ids(selected_spells)
    buffer = spell_printer.create_spelllist()
    buffer.seek(0)

    return send_file(buffer, mimetype='application/pdf')


@app.route('/add-creature', methods=['GET', 'POST'])
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


@app.route('/edit-creature/<id>', methods=['GET', 'POST'])
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


@app.route('/get-spellbook-spell-ids')
def get_spellbook_spells():
    spellbook_spell_ids = []
    if current_user.is_authenticated:
        cached = cache.get(f'spellbook_spell_ids:{current_user.user_id}')
        if cached:
            return cached
        spellbook_spell_ids = [spell.spell_id for spell in
                               current_user.spellbook.spells]
        cache.set(f'spellbook_spell_ids:{current_user.user_id}',
                  spellbook_spell_ids, 99999)

    return jsonify(spellbook_spell_ids)
