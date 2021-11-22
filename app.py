import os
import sys

home = os.environ['PROJECT_HOME']
sys.path.append(home + '/geocatalog/sources/lib')

from geocatalog import create_app
from geocatalog.routes import main_routes


app = create_app(home + os.environ['CFG_FILE'])

for view_id in main_routes:
    view_class = main_routes[view_id]['class']
    view = view_class.as_view(view_id)

    for rule in main_routes[view_id]['rules']:
        app.add_url_rule(rule, view_func=view)

if __name__ == '__main__':
    app.run()
