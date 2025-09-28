from app.models import Character, db


class CharacterCreator:
    def __init__(self, data, user):
        self.name = data.get('name', '')
        self.user_id = user.user_id
        self.message = ''

    def validate(self):
        if Character.query.filter_by(name=self.name, user_id=self.user_id).first():
            self.message = 'У вас уже є такий персонаж'
            return False

        if not self.name:
            self.message = 'Ім\'я порожнє'
            return False
        return True


    def create(self):
        character = Character(name=self.name, user_id=self.user_id)
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)
        return character
