from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from apps.responsible_disc import models


@receiver(post_save, sender=models.Vulnerability)
def vulnerability_creator_permissions(sender, instance=None, created=False, **kwargs):
    # assign vulnerability permission to user
    if created:
        perms = ["responsible_disc.view_vulnerability", "responsible_disc.change_vulnerability",
                 "responsible_disc.delete_vulnerability"]
        for perm in perms:
            assign_perm(perm, instance.user, instance)
