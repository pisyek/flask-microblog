from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import logging
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors

if not app.debug:
    LOG_PATH = os.path.join(Config.BASE_PATH, 'logs')
    
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    LOG_FILE = os.path.join(LOG_PATH, 'microblog.log')

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10240,
                                    backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
