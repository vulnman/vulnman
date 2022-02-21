from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.methodologies import constants


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


class AssetTask(VulnmanProjectModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=0)
    asset_webapp = models.ForeignKey('assets.WebApplication', on_delete=models.SET_NULL, null=True, blank=True)
    asset_webrequest = models.ForeignKey('assets.WebRequest', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [
            ("task", "project", "asset_webrequest"),
            ("task", "project", "asset_webapp")
        ]

    @property
    def asset(self):
        if self.asset_webapp:
            return self.asset_webapp
        elif self.asset_webrequest:
            return self.asset_webrequest
