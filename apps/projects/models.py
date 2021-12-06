from uuid import uuid4
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from apps.projects import constants


class Project(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer = models.CharField(max_length=64)
    report_default_title = models.CharField(max_length=64, default="Pentest Report")
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def has_vulns_with_severity(self, severity):
        for vuln in self.vulnerability_set.all():
            if vuln.get_severities()[0] == severity:
                return True
        return False

    class Meta:
        ordering = ["-date_updated"]


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=constants.PROJECT_MEMBER_CHOICES)

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:project-member-delete", kwargs={'pk': self.pk})

    class Meta:
        unique_together = [('project', 'user')]


class ProjectContact(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=24, blank=True, null=True)
    pgp_key = models.TextField(blank=True, null=True, verbose_name="PGP-Key")

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        unique_together = [('project', 'email')]
        verbose_name_plural = "Contacts"
        verbose_name = "Contact"


class Scope(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=32)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('project', 'name')]
        verbose_name_plural = "Scopes"
