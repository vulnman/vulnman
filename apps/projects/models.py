import secrets
from uuid import uuid4
from guardian.shortcuts import assign_perm, remove_perm
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy


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

    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('projects.Client', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.PositiveIntegerField(choices=PENTEST_STATUS_CHOICES, default=PENTEST_STATUS_OPEN)
    name = models.CharField(max_length=128)
    pentest_method = models.PositiveIntegerField(choices=PENTEST_METHOD_CHOICES, default=PENTEST_METHOD_GREYBOX)
    cvss_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def archive_project(self):
        for contributor in self.projectcontributor_set.all():
            remove_perm("projects.change_project", contributor.user, self)
            remove_perm("projects.delete_project", contributor.user, self)
        remove_perm("projects.change_project", self.creator, self)
        remove_perm("projects.delete_project", self.creator, self)
        remove_perm("projects.add_contributor", self.creator, self)

    def is_contributor(self, user):
        if self.creator == user:
            return True
        return self.projectcontributor_set.filter(user=user).exists()

    def get_assets(self):
        assets = list(self.webapplication_set.all()) + list(self.webrequest_set.all()) + list(self.host_set.all())
        return assets

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
        perms = ["projects.add_contributor", "projects.view_project", "projects.change_project", "projects.delete_project"]
        for perm in perms:
            assign_perm(perm, user_or_group=self.creator, obj=self)

    def get_open_todos(self):
        return self.assettask_set.filter(~Q(status=0))

    def get_compromised_accounts(self):
        return self.useraccount_set.filter(account_compromised=True)

    class Meta:
        ordering = ["-date_updated"]
        permissions = [
            ("pentest_project", "Pentest Project"),
            ("add_contributor", "Add Contributor")
        ]


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
    POSITION_ORGANISATIONAL = "org"
    POSITION_TECHNICAL = "tech"

    POSITION_CHOICES = [
        (POSITION_ORGANISATIONAL, "Organisational"),
        (POSITION_TECHNICAL, "Technical")
    ]

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
    position = models.CharField(max_length=64, choices=POSITION_CHOICES)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Client Contact"
        verbose_name_plural = "Client Contacts"


class ProjectContributor(models.Model):
    ROLE_PENTESTER = "pentester"

    CONTRIBUTOR_ROLE_CHOICES = [
        (ROLE_PENTESTER, "Pentester"),
    ]

    uuid = models.UUIDField(default=uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=16, choices=CONTRIBUTOR_ROLE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_role_permission_map(self):
        # TODO: maybe not allow a pentester to delete a project?
        # There is no endpoint for this at the moment
        # but this may change soon.
        return {
            ProjectContributor.ROLE_PENTESTER: [
                "projects.view_project", "projects.change_project",
                "projects.delete_project"]
        }

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        self.assign_role_permissions(self.role)
        return obj

    def assign_role_permissions(self, role):
        perm_map = self.get_role_permission_map()
        if perm_map.get(role):
            for perm in perm_map[role]:
                assign_perm(perm, user_or_group=self.user, obj=self.project)

    def clear_perms(self):
        perm_map = self.get_role_permission_map()
        for role in self.get_role_permission_map().keys():
            for perm in perm_map[role]:
                remove_perm(perm, self.user, self.project)

    def get_project(self):
        return self.project

    class Meta:
        unique_together = [("user", "project")]


class ProjectAPIToken(models.Model):
    key = models.CharField(max_length=512, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    @classmethod
    def generate_key(cls):
        return secrets.token_hex(64)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:token-delete", kwargs={"pk": self.pk})
