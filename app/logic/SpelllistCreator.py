from app.models import Spellbook, Character, Spell
from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template
import os
from xhtml2pdf.files import pisaFileObject


class SpelllistCreator:
    def __init__(self):
        spells = []

    def get_spells_from_spellbook(self, spellbook_id):
        spellbook = Spellbook.query.get(spellbook_id)
        self.spells = [spell.spell for spell in spellbook.spells]

    def get_spells_from_character(self, character_id):
        character = Character.query.get(character_id)
        self.spells = [spell.spell for spell in character.spells]

    def get_spells_by_ids(self, ids):
        self.spells = Spell.query.filter(Spell.spell_id.in_(ids)).all()


    def create_spelllist(self):
        buffer = BytesIO()

        html_content = render_template('spelllist.html', spells=self.spells)
        pisaFileObject.getNamedFile = lambda self: self.uri

        pisa.CreatePDF(html_content, dest=buffer, encoding='UTF-8', link_callback=link_callback)

        return buffer


def link_callback(uri, rel):
    return os.path.join(os.getcwd(), 'app', 'static', 'css', 'fonts', uri)
