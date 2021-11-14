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
