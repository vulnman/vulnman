from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'

    def ready(self):
        from apps.account.signals import populate_groups_and_permission
        post_migrate.connect(populate_groups_and_permission, sender=self)
