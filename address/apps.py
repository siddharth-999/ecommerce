from django.apps import AppConfig


class AddressConfig(AppConfig):
    name = 'address'

    def ready(self):
        from address import signals