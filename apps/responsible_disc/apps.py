from django.apps import AppConfig


class ResponsibleDiscConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.responsible_disc'

    def ready(self):
        from apps.responsible_disc import signals
