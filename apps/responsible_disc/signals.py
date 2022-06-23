import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from apps.responsible_disc import models


@receiver(post_save, sender=models.Vulnerability)
def vulnerability_creator_permissions(sender, instance=None, created=False, **kwargs):
    # assign vulnerability permission to user
    if created:
        perms = ["responsible_disc.view_vulnerability", "responsible_disc.change_vulnerability",
                 "responsible_disc.delete_vulnerability", "responsible_disc.invite_vendor"]
        for perm in perms:
            assign_perm(perm, instance.user, instance)


@receiver(post_delete, sender=models.ImageProof)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
