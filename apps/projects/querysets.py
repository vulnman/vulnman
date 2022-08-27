from django.db import models
from guardian.shortcuts import get_objects_for_user


class ProjectQuerySet(models.QuerySet):
    def for_user(self, user, perms="projects.view_project"):
        qs = get_objects_for_user(user, perms, self.model, use_groups=False,
                                  accept_global_perms=False, with_superuser=False)
        return qs


class ProjectManager(models.Manager):
    pass
