"""
 Базовый класс для сервисов
"""

from geocatalog.service.service_manager import SERVICE_MANAGER


class Service:

    def __init__(self, id):
        self.id = id

    def register(self):
        return SERVICE_MANAGER.register_service(self)

    def unregister(self):
        return SERVICE_MANAGER.unregister_service(self)
