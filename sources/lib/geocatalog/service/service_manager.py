"""
Менеджер сервисов. Синглетон. Автоматом создается при импорте модуля.

Предлагает на экспорт функцию get_service, выдающую по идентификатору сервис,
зарегистрированный в менеджере сервисов.
"""


class ServiceManager:

    def __init__(self):
        self.services = {}

    def register_service(self, service):
        if service.id in self.services:
            return False

        self.services[service.id] = service

        return True

    def unregister_service(self, service):
        if service.id not in self.services:
            return False

        self.services.pop(service.id)

        return True

    def get_service(self, id):
        return self.services.get(id)


SERVICE_MANAGER = ServiceManager()


def get_service(id):
    return SERVICE_MANAGER.get_service(id)
