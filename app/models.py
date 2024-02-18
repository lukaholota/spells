from app.db import db
from flask_login import UserMixin


class Spell(db.Model):
    spell_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    level = db.Column(db.String)
    school = db.Column(db.String)
    casting_time = db.Column(db.String)
    range = db.Column(db.String)
    components = db.Column(db.String)
    duration = db.Column(db.String)
    description = db.Column(db.String)
    has_ritual = db.Column(db.String)
    has_concentration = db.Column(db.String)
    source = db.Column(db.String, nullable=False, server_default='Книга гравця')

    classes = db.relationship('SpellClasses', backref='spell')
    races = db.relationship('SpellRaces', backref='spell')


class SpellClasses(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.spell_id'))
    class_name = db.Column(db.String)


class SpellRaces(db.Model):
    race_id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.spell_id'))
    race_name = db.Column(db.String)


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    login = db.Column(db.String(1000))
    spellbook = db.relationship('Spellbook', backref='user', uselist=False)
    characters = db.relationship('Character', backref='user')

    def get_id(self):
        return self.user_id


class Spellbook(db.Model):
    spellbook_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    spells = db.relationship('SpellbookSpells', backref='spellbook')


class SpellbookSpells(db.Model):
    spellbook_spell_id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.spell_id'))
    spellbook_id = db.Column(db.Integer, db.ForeignKey('spellbook.spellbook_id'))
    spell = db.relationship('Spell', uselist=False)


class Character(db.Model):
    character_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    spells = db.relationship('CharacterSpells', backref='character')


class CharacterSpells(db.Model):
    character_spell_id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.spell_id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    spell = db.relationship('Spell', uselist=False)


class Creature(db.Model):
    creature_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    name_eng = db.Column(db.String)
    size = db.Column(db.String)
    type = db.Column(db.String)
    alignment = db.Column(db.String)
    source = db.Column(db.String)
    ac = db.Column(db.String)
    hp = db.Column(db.String)
    speed = db.Column(db.String)
    strength = db.Column(db.String)
    dexterity = db.Column(db.String)
    constitution = db.Column(db.String)
    intelligence = db.Column(db.String)
    wisdom = db.Column(db.String)
    charisma = db.Column(db.String)
    skills = db.Column(db.String)
    senses = db.Column(db.String)
    languages = db.Column(db.String)
    challenge = db.Column(db.String)
    damage_immunity = db.Column(db.String)
    damage_resistance = db.Column(db.String)
    condition_immunity = db.Column(db.String)
    saving_throws = db.Column(db.String)
    special_abilities = db.Column(db.String)
    actions = db.Column(db.String)
    reactions = db.Column(db.String)
    legendary_actions = db.Column(db.String)
    description = db.Column(db.String)
    lair_info = db.Column(db.String)
    lair_actions = db.Column(db.String)
    region_effects = db.Column(db.String)
    proficiency_bonus = db.Column(db.String)
    xp = db.Column(db.String)
