from django.apps import AppConfig


class AssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assets'

    def ready(self):
        # TODO: use this one again
        # from apps.assets import signals
        pass