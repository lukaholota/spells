from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from app.db import db
from flask_migrate import Migrate
from flask_caching import Cache
from flask_marshmallow import Marshmallow

from app.settings import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['CACHE_TYPE'] = 'simple'

auth = HTTPBasicAuth()
login_manager = LoginManager()
login_manager.login_view = '/sign-in'
login_manager.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

cache = Cache(app)

ma = Marshmallow(app)

from app.models import User
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


from app.app_routes import *
