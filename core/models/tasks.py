from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.methodologies import constants
from apps.assets.models import ASSET_TYPES_CHOICES


TASK_STATUS_CHOICES = [
    (0, "Open"),
    (1, "Closed"),
    (2, "To Review"),
    (3, "Not Tested"),
    (4, "Not Applicable")
]


class Task(VulnmanModel):
    task_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.task_id

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = [("task_id",)]


class TaskCondition(VulnmanModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    asset_type = models.CharField(choices=ASSET_TYPES_CHOICES, max_length=128)
    condition = models.CharField(max_length=256, null=True, blank=True)
    is_regex = models.BooleanField(default=False)
    on_pentest = models.BooleanField(default=False)

    class Meta:
        unique_together = [('task', 'asset_type', 'condition', 'is_regex')]


class AssetTask(VulnmanProjectModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(
        default=0, choices=TASK_STATUS_CHOICES)
    asset_webapp = models.ForeignKey(
        'assets.WebApplication', on_delete=models.CASCADE, null=True,
        blank=True)
    asset_webrequest = models.ForeignKey(
        'assets.WebRequest', on_delete=models.CASCADE, null=True, blank=True)
    asset_host = models.ForeignKey(
        "assets.Host", null=True, blank=True, on_delete=models.CASCADE
    )
    asset_service = models.ForeignKey(
        "assets.Service", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [
            ("task", "project", "asset_webrequest"),
            ("task", "project", "asset_webapp"),
            ("task", "project", "asset_service"),
            ("task", "project", "asset_host")
        ]

    @property
    def asset(self):
        if self.asset_webapp:
            return self.asset_webapp
        elif self.asset_webrequest:
            return self.asset_webrequest
        elif self.asset_service:
            return self.asset_service
        elif self.asset_host:
            return self.asset_host

    def get_status_display(self):
        for s in TASK_STATUS_CHOICES:
            if self.status == s[0]:
                return s[1]

    def get_absolute_url(self):
        return reverse_lazy(
            "projects:methodologies:project-task-detail", kwargs={"pk": self.pk})


    @property
    def name(self):
        return self.task.name
