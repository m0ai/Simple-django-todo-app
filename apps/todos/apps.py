from django.apps import AppConfig

class TodosConfig(AppConfig):
    name = 'apps.todos'

    def ready(self):
        from . import signals
