from django.apps import AppConfig


class MedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Med'

    def ready(self):
        import Med.signals