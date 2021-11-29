from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class WebApplication(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    latest_version = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name
