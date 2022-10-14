import os.path
import secrets
from uuid import uuid4
from guardian.shortcuts import assign_perm, remove_perm
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from apps.projects import querysets


class Project(models.Model):
    PENTEST_METHOD_WHITEBOX = 0
    PENTEST_METHOD_GREYBOX = 1
    PENTEST_METHOD_BLACKBOX = 2

    PENTEST_METHOD_CHOICES = [
        (PENTEST_METHOD_WHITEBOX, "Whitebox"),
        (PENTEST_METHOD_GREYBOX, "Greybox"),
        (PENTEST_METHOD_BLACKBOX, "Blackbox")
    ]

    PENTEST_STATUS_OPEN = 0
    PENTEST_STATUS_CLOSED = 1
    PENTEST_STATUS_INPROGRESS = 2

    PENTEST_STATUS_CHOICES = [
        (PENTEST_STATUS_CLOSED, "Closed"),
        (PENTEST_STATUS_OPEN, "Open"),
        (PENTEST_STATUS_INPROGRESS, "In Progress")
    ]
    objects = querysets.ProjectManager.from_queryset(querysets.ProjectQuerySet)()
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('projects.Client', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.PositiveIntegerField(choices=PENTEST_STATUS_CHOICES, default=PENTEST_STATUS_OPEN)
    name = models.CharField(max_length=128)
    pentest_method = models.PositiveIntegerField(choices=PENTEST_METHOD_CHOICES, default=PENTEST_METHOD_GREYBOX)
    cvss_required = models.BooleanField(default=False, verbose_name="CVSS required")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("projects:project-detail", kwargs={"pk": self.pk})

    def archive_project(self):
        for contributor in self.projectcontributor_set.all():
            remove_perm("projects.change_project", contributor.user, self)
            remove_perm("projects.delete_project", contributor.user, self)
        remove_perm("projects.change_project", self.creator, self)
        remove_perm("projects.delete_project", self.creator, self)
        remove_perm("projects.add_contributor", self.creator, self)

    def get_assets(self):
        assets = list(self.webapplication_set.all()) + list(self.host_set.all()) + \
                 list(self.service_set.all())
        return assets

    def get_scope(self):
        # used in default report template
        scope_assets = list(self.webapplication_set.all()) + list(self.host_set.all())
        return scope_assets

    def get_draft_report(self):
        if self.pentestreport_set.filter(report_type="draft", name="").exists():
            return self.pentestreport_set.get(report_type="draft", name="")
        return None

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        self.assign_creator_permissions()
        return obj

    def assign_creator_permissions(self):
        if not self.creator:
            return
        perms = [
            "projects.add_contributor", "projects.view_project", "projects.change_project", "projects.delete_project"
        ]
        for perm in perms:
            assign_perm(perm, user_or_group=self.creator, obj=self)

    def get_open_todos(self):
        return self.assettask_set.filter(~Q(status=1))

    def get_compromised_accounts(self):
        return self.useraccount_set.filter(account_compromised=True)

    class Meta:
        ordering = ["-date_updated"]
        permissions = [
            ("pentest_project", "Pentest Project"),
            ("add_contributor", "Add Contributor")
        ]


def customer_logo_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "logo.%s" % ext
    return "uploads/customers/%s/files/%s" % (instance.pk, filename)


class Client(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, unique=True)
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    zip = models.IntegerField()
    homepage = models.URLField(blank=True, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to=customer_logo_upload_path)

    def __str__(self):
        return self.name

    def get_full_address(self):
        return "%s, %s (%s)" % (self.city, self.zip, self.country)

    def get_homepage_display(self):
        if self.homepage:
            return self.homepage
        return "-"

    def get_absolute_url(self):
        return reverse_lazy("clients:client-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("clients:client-delete", kwargs={"pk": self.pk})


class ClientContact(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                related_name="clientcontact_set")
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

    def get_absolute_delete_url(self):
        return reverse_lazy("clients:contact-delete", kwargs={"pk": self.pk})


class ProjectContributor(models.Model):
    ROLE_PENTESTER = "pentester"
    ROLE_READ_ONLY = "ro"

    CONTRIBUTOR_ROLE_CHOICES = [
        (ROLE_PENTESTER, "Pentester"),
        (ROLE_READ_ONLY, "Read Only")
    ]

    ROLE_PENTESTER_PERMISSIONS = ["projects.view_project", "projects.change_project"]
    ROLE_READ_ONLY_PERMISSIONS = ["projects.view_project"]

    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=16, choices=CONTRIBUTOR_ROLE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    date_confirmed = models.DateTimeField(null=True, blank=True)
    invite_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        if self.user:
            return self.user.username
        return self.invite_email

    def get_project(self):
        return self.project

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:contributor-delete", kwargs={"pk": self.pk})

    class Meta:
        unique_together = [("user", "project")]
        ordering = ["-date_created"]


class ProjectAPIToken(models.Model):
    key = models.CharField(max_length=512, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    date_valid = models.DateField()

    @classmethod
    def generate_key(cls):
        return secrets.token_hex(64)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:token-delete", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-date_valid"]


def project_file_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return "uploads/projects/%s/files/%s" % (instance.project.pk, filename)


class ProjectFile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    file = models.FileField(upload_to=project_file_upload_path)

    def __str__(self):
        return self.name

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse_lazy("projects:file-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:file-delete", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-date_created"]
