from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from geocatalog.service import ConfigService


db = SQLAlchemy()


def create_app(cfg_file):
    app = Flask(__name__)

    config = ConfigService(cfg_file)
    config.register()

    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_dns()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
