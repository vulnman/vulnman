from django.apps import AppConfig


class FindingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.findings'

    def ready(self):
        import apps.findings.signals
