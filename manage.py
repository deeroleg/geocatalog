# manage.py

import os
import sys

home = os.environ['PROJECT_HOME']
sys.path.append(home + '/geocatalog/sources/lib')


from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from geocatalog import create_app, db
from geocatalog.models.region import Region
from geocatalog.models.city import City

app = create_app(home + os.environ['CFG_FILE'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
