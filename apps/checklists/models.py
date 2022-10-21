from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from vulnman.models import VulnmanProjectModel, VulnmanModel
from apps.checklists import querysets
from apps.assets.models import ASSET_TYPES_CHOICES


class Technology(VulnmanModel):
    name = models.CharField(max_length=128)
    programming_language = models.CharField(max_length=128, blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)
    version = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        unique_together = [
            ('name', 'version')
        ]


class AssetTechnology(VulnmanProjectModel):
    ASSET_TYPES_CHOICES = [
        ("webapplication", "Web Application"),
        ("host", "Host"),
        ("service", "Service")
    ]
    objects = querysets.AssetTechnologyManager.from_queryset(querysets.AssetTechnologyQuerySet)()
    asset_type = models.CharField(max_length=64, choices=ASSET_TYPES_CHOICES, default="webapplication")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    asset = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-date_updated"]


class BaseChecklistTask(VulnmanModel):
    task_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.TextField()

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = [("task_id",)]
        abstract = True

    def __str__(self):
        return self.task_id


class ChecklistTask(BaseChecklistTask):
    pass


class Condition(models.Model):
    task = models.ForeignKey('checklists.ChecklistTask', on_delete=models.CASCADE)
    on_asset_type = models.CharField(choices=ASSET_TYPES_CHOICES, max_length=128)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = [('task', 'on_asset_type', 'name', 'value')]


class ProjectTask(BaseChecklistTask):
    STATUS_OPEN = 1
    STATUS_CLOSED = 2
    STATUS_REVIEW = 3
    STATUS_NOT_TESTED = 4
    STATUS_NOT_APPLICABLE = 5

    TASK_STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
        (STATUS_REVIEW, "To Review"),
        (STATUS_NOT_TESTED, "Not Tested"),
        (STATUS_NOT_APPLICABLE, "Not Applicable")
    ]
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=STATUS_OPEN, choices=TASK_STATUS_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        "model__in": ['Host', 'Service', 'assets.WebApplication']
    })
    object_id = models.UUIDField()
    asset = GenericForeignKey("content_type", "object_id")

    def get_creator_display(self):
        if self.creator:
            return self.creator.username
        return "vulnman bot"
