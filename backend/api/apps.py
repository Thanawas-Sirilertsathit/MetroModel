from django.apps import AppConfig

class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from . import model_registry
        model_registry.init_models()
