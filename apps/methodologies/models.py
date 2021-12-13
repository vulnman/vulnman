from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from vulnman.models import VulnmanModel, VulnmanProjectModel
from apps.methodologies import constants


class Methodology(VulnmanModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('methodology:methodology-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse_lazy('methodology:methodology-update', kwargs={'pk': self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy('methodology:methodology-delete', kwargs={'pk': self.pk})

    def get_absolute_update_url(self):
        return reverse_lazy('methodology:methodology-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date_updated"]


class Task(VulnmanModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    methodology = models.ForeignKey(Methodology, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        unique_together = [("name", "methodology")]


class ProjectMethodology(VulnmanProjectModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-date_updated"]
        unique_together = [('name', 'project')]
        verbose_name = "Project Methodology"
        verbose_name_plural = "Project Methodologies"

    def get_open_tasks(self):
        return self.projecttask_set.exclude(status="done")

    def get_absolute_url(self):
        return reverse_lazy("projects:methodology:project-methodology-detail", kwargs={"pk": self.pk})

    def get_absolute_delete_url(self):
        return reverse_lazy("projects:methodology:project-methodology-delete", kwargs={"pk": self.pk})

    def get_absolute_update_url(self):
        return reverse_lazy("projects:methodology:project-methodology-update", kwargs={"pk": self.pk})

    def get_tasks_todo(self):
        return self.projecttask_set.filter(status="todo")

    def get_tasks_progress(self):
        return self.projecttask_set.filter(status="progress")

    def get_tasks_done(self):
        return self.projecttask_set.filter(status="done")


class ProjectTask(VulnmanProjectModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    methodology = models.ForeignKey(ProjectMethodology, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_projecttask_set", blank=True)
    status = models.CharField(max_length=28, choices=constants.TASK_STATUS_CHOICES, default="todo")

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "Project Task"
        verbose_name_plural = "Project Tasks"
        unique_together = [("name", "methodology")]

    def __str__(self):
        return self.name
