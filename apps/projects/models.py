import json
from uuid import uuid4
from django.db import models
from django.db.models.functions import Cast
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Project(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('projects.Client', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    report_default_title = models.CharField(max_length=64, default="Assessment Report", blank=True)
    is_archived = models.BooleanField(default=False)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def has_vulns_with_severity(self, severity):
        for vuln in self.vulnerability_set.all():
            if vuln.get_severities()[0] == severity:
                return True
        return False

    def get_critical_vulnerabilities_count(self):
        return self.get_critical_vulnerabilities(count=True)

    def get_critical_vulnerabilities(self, count=False, include_only_verified=True):
        qs = self.vulnerability_set.filter(template__severity=4, verified=include_only_verified)
        if count:
            return qs.count()
        return qs

    def get_high_vulnerabilities_count(self):
        return self.get_high_vulnerabilities(count=True)

    def get_high_vulnerabilities(self, count=False, include_only_verified=True):
        qs = self.vulnerability_set.filter(template__severity=3, verified=include_only_verified)
        if count:
            return qs.count()
        return qs

    def get_medium_vulnerabilities(self, count=False, include_only_verified=True):
        qs = self.vulnerability_set.filter(template__severity=2, verified=include_only_verified)
        if count:
            return qs.count()
        return qs

    def get_medium_vulnerabilities_count(self):
        return self.get_medium_vulnerabilities(count=True)

    def get_low_vulnerabilities(self, count=False, include_only_verified=True):
        qs = self.vulnerability_set.filter(template__severity=1, verified=include_only_verified)
        if count:
            return qs.count()
        return qs

    def get_low_vulnerabilities_count(self):
        return self.get_low_vulnerabilities(count=True)

    def get_informational_vulnerabilities(self, count=False, include_only_verified=True):
        qs = self.vulnerability_set.filter(template__severity=0, verified=include_only_verified)
        if count:
            return qs.count()
        return qs

    def get_informational_vulnerabilities_count(self):
        return self.get_informational_vulnerabilities(count=True)

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_retrieve_permission(self, request):
        if request.user == self.creator:
            return True
        return False

    def get_latest_command_history(self):
        return self.commandhistoryitem_set.order_by("-date_updated")[:10]

    class Meta:
        ordering = ["-date_updated"]
        permissions = [
            ("pentest_project", "Pentest Project"),
        ]


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


class Client(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, unique=True)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    zip = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("clients:client-detail", kwargs={"pk": self.pk})


class ClientContact(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=24, blank=True, null=True)
    pgp_key = models.TextField(blank=True, null=True, verbose_name="PGP-Key")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    position = models.CharField(max_length=64)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Client Contact"
        verbose_name_plural = "Client Contacts"
