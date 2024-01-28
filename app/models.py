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
    spellbook = db.relationship('Spellbook', backref='user')

    def get_id(self):
        return self.user_id


class Spellbook(db.Model):
    spellbook_id = db.Column(db.Integer, primary_key=True)
    spells = db.relationship('SpellbookSpells', backref='spellbook')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


class SpellbookSpells(db.Model):
    spellbook_spell_id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey('spell.spell_id'))
    spellbook_id = db.Column(db.Integer, db.ForeignKey('spellbook.spellbook_id'))
