from flask import Flask
from flask_httpauth import HTTPBasicAuth
from app.db import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dnddlaukraincow@31.131.17.213:5454/postgres'
auth = HTTPBasicAuth()

db.init_app(app)
migrate = Migrate(app, db)

from app.app_routes import *
