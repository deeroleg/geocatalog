from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from geocatalog.service import ConfigService


db = SQLAlchemy()


def create_app(cfg_file):
    from geocatalog.routes import main_routes
    
    app = Flask(__name__)

    config = ConfigService(cfg_file)
    config.register()

    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_dns()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    for view_id in main_routes:
        view_class = main_routes[view_id]['class']
        view = view_class.as_view(view_id)

        for rule in main_routes[view_id]['rules']:
            app.add_url_rule(rule, view_func=view)

    return app
