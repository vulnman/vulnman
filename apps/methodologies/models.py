from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from uuid import uuid4
from vulnman.models import VulnmanModel


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
