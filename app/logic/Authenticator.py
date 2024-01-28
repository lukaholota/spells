from app.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user


class Authenticator:
    def __init__(self, data):
        self.login = data.get('login', '')
        self.password = data.get('password', '')
        self.remember_me = True if data.get('remember_me', '') else False

    def check_if_exists(self):
        user = User.query.filter_by(login=self.login).first()
        if user:
            return user

    def add_new_user(self):
        new_user = User(login=self.login, password=generate_password_hash(self.password))

        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)

        login_user(new_user, remember=self.remember_me)

    def sign_in(self):
        user = User.query.filter_by(login=self.login).first()

        if user and check_password_hash(user.password, self.password):
            login_user(user, remember=self.remember_me)
            return True
        return False


