from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from app.db import db
from flask_migrate import Migrate
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dnddlaukraincow@31.131.17.213:5454/postgres'

auth = HTTPBasicAuth()
login_manager = LoginManager()
login_manager.login_view = '/sign-in'
login_manager.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)


from app.models import User
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


from app.app_routes import *
