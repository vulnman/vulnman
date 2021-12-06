from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from uuid import uuid4


class Employee(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [("project", "email")]

    def __str__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.last_name:
            return self.last_name
        return self.email

    def get_absolute_url(self):
        return reverse_lazy('projects:social:employee-detail', kwargs={'pk': self.pk})


class Credential(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    username = models.CharField(max_length=256)
    cleartext_password = models.CharField(max_length=255, blank=True, null=True)
    hashed_password = models.CharField(max_length=512, blank=True, null=True)
    location_found = models.CharField(max_length=512)
    valid_services = models.ManyToManyField('networking.Service')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
