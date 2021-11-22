"""
Класс для хранения конфигурации системы
"""

import yaml

from geocatalog.service import Service


class ConfigService(Service):

    def __init__(self, cfg_file=None):
        super().__init__('config')

        self.data = {}

        if cfg_file:
            with open(cfg_file, 'r') as stream:
                self.data = yaml.safe_load(stream)

    def get(self, item, default=None):
        return self.data.get(item, default)

    def __getitem__(self, item):
        return self.data[item]

    def get_dns(self):
        data = self.get('database')
        if data:
            host = data.get('host') or '127.0.0.1'
            port = data.get('port') or 5432
            name = data.get('name')
            user = data.get('user')
            password = data.get('password')
            return 'postgresql://%s:%s@%s:%s/%s' % (user, password, host, port, name)

        return None
