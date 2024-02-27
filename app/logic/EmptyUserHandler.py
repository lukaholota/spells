from app.models import User
from flask import redirect
from app.logic import CharacterCreator, SpellbookSaver, SeparateCharacterSpellSaver
from flask_login import logout_user


class EmptyUserHandler:
    def __init__(self, current_user):
        self.user: User = current_user
        self.empty_user = None

    def check_if_empty(self):
        if self.user.is_authenticated:
            return self.user.login == ''
        return False

    def handle_empty(self):
        logout_user()
        return redirect('/sorry-registration')

    def transfer_data(self):
        self.empty_user: User = User.query.filter_by(login='').first()

        self.handle_spellbook()
        self.handle_characters()

    def handle_spellbook(self):
        spellbook_saver = SpellbookSaver.SpellbookSaver(self.user)

        for spell in self.empty_user.spellbook.spells:
            spell_id = spell.spell_id
            spellbook_saver.add_spell_to_spellbook(spell_id)

    def handle_characters(self):
        for character in self.empty_user.characters:
            data = {'name': character.name}
            character_creator = CharacterCreator.CharacterCreator(data, self.user)
            new_character = character_creator.create()

            for spell in character.spells:
                character_spells_saver = SeparateCharacterSpellSaver.SeparateCharacterSpellSaver(new_character.character_id, spell.spell_id)
                character_spells_saver.save()
