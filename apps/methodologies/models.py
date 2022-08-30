from django.db import models
from django.urls import reverse_lazy
from vulnman.models import VulnmanModel, VulnmanProjectModel
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
    name = models.CharField(max_length=128, default="always")
    condition = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = [('task', 'asset_type', 'name', 'condition')]


class AssetTask(VulnmanProjectModel):
    STATUS_OPEN_ICON = "fa fa-question"
    STATUS_CLOSED_ICON = "fa fa-check"
    STATUS_TO_REVIEW_ICON = "fa fa-user-group"
    STATUS_NOT_TESTED_ICON = "fa fa-exclamation"
    STATUS_NOT_APPLICABLE_ICON = "fa fa-xmark"

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(
        default=0, choices=TASK_STATUS_CHOICES)
    asset_webapp = models.ForeignKey(
        'assets.WebApplication', on_delete=models.CASCADE, null=True,
        blank=True)
    asset_host = models.ForeignKey(
        "assets.Host", null=True, blank=True, on_delete=models.CASCADE
    )
    asset_service = models.ForeignKey(
        "assets.Service", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [
            ("task", "project", "asset_webapp"),
            ("task", "project", "asset_service"),
            ("task", "project", "asset_host")
        ]

    @property
    def asset(self):
        if self.asset_webapp:
            return self.asset_webapp
        elif self.asset_service:
            return self.asset_service
        elif self.asset_host:
            return self.asset_host

    def get_status_icon(self):
        if self.status == 0:
            return self.STATUS_OPEN_ICON
        elif self.status == 1:
            return self.STATUS_CLOSED_ICON
        elif self.status == 2:
            return self.STATUS_TO_REVIEW_ICON
        elif self.status == 3:
            return self.STATUS_NOT_TESTED_ICON
        elif self.status == 4:
            return self.STATUS_NOT_APPLICABLE_ICON

    def get_absolute_url(self):
        return reverse_lazy("projects:methodologies:project-task-detail", kwargs={"pk": self.pk})

    @property
    def name(self):
        return self.task.name

    def get_creator_display(self):
        if self.creator:
            return self.creator.username
        return "Vulnman Server"
