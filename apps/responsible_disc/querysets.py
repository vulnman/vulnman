from django.db import models
from guardian.shortcuts import get_objects_for_user


class VulnerabilityQuerySet(models.QuerySet):
    def for_user(self, user, perm="responsible_disc.view_vulnerability"):
        qs = get_objects_for_user(user, perm, self.model, use_groups=False,
                                  with_superuser=False, accept_global_perms=False)
        return qs
