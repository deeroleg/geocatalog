"""
Класс - хранилище соединений с базами данных и кэшом
"""

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from geocatalog.service import Service


class KeeperService(Service):

    def __init__(self):
        super().__init__('keeper')

        self.db_engine = None
        self.db_session = None
        self.db_session_factory = None

    def init_db(self, host='127.0.0.1', port=5432, name=None, user=None, password=None):
        dsn = 'postgresql://%s:%s@%s:%s/%s' % (user, password, host, port, name)

        self.db_engine = create_engine(dsn, convert_unicode=True)

        self.db_session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self.db_engine
        )

    def get_db_session(self):
        if not self.db_session:
            self.connect()

        return self.db_session

    def connect(self):
        if not self.db_session:
            self.db_session = self.db_session_factory()

    def cleanup(self):
        if self.db_session:
            self.db_session.close()
            self.db_session = None

    def shutdown(self):
        self.cleanup()

        self.db_session_factory = None

        if self.db_engine:
            self.db_engine.dispose()
            self.db_engine = None

        self.memd_disconnect()
