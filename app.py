import os
import sys

home = os.environ['PROJECT_HOME']
sys.path.append(home + '/geocatalog/sources/lib')

from geocatalog import create_app

app = create_app(home + os.environ['CFG_FILE'])


if __name__ == '__main__':
    app.run()
