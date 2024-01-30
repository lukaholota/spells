from app.models import Character, db, CharacterSpells


class CharacterDeleter:
    def __init__(self, character_id):
        self.character_id = character_id

    def delete(self):
        CharacterSpells.query.filter_by(character_id=self.character_id).delete()
        Character.query.filter_by(character_id=self.character_id).delete()
        db.session.commit()
