from django.apps import AppConfig


class ParticipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Participes'
    def ready(self):
        import Participes.signals
