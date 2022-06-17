from django.db import models
from django.conf import settings
from uuid import uuid4


class VulnmanModel(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class VulnmanProjectModel(VulnmanModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_project(self):
        return self.project
