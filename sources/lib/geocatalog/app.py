import os
import sys

home = os.environ['PROJECT_HOME']
sys.path.append(home + '/geocatalog/sources/lib')

from flask import Flask

from geocatalog.service import get_service
from geocatalog.service import ConfigService, KeeperService
from geocatalog.routes import main_routes


app = Flask(__name__)

config = ConfigService(home + os.environ['CFG_FILE'])
config.register()

keeper = KeeperService()
keeper.init_db(
    host=config['database']['host'],
    port=config['database']['port'],
    name=config['database']['name'],
    user=config['database']['user'],
    password=config['database']['password']
)
keeper.register()

@app.before_request
def before_request():
    get_service('keeper').connect()

@app.teardown_request
def teardown_request(e):
    get_service('keeper').cleanup()

for view_id in main_routes:
    view_class = main_routes[view_id]['class']
    view = view_class.as_view(view_id)

    for rule in main_routes[view_id]['rules']:
        app.add_url_rule(rule, view_func=view)

if __name__ == '__main__':
    app.run()
