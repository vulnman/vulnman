from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from guardian.shortcuts import get_perms, remove_perm, assign_perm
from apps.projects.models import ProjectContributor, ProjectAPIToken


@receiver(pre_delete, sender=ProjectContributor)
def delete_contributor_from_project(sender, instance, **kwargs):
    if not instance.user:
        # remove a contributor that has not yet confirmed invitation
        return
    perms = get_perms(instance.user, instance.project)
    for perm in perms:
        remove_perm(perm, user_or_group=instance.user, obj=instance.project)
    # ensure that the API tokens are wiped, when a contributor is deleted
    # otherwise the contributor may still have access to the project
    ProjectAPIToken.objects.filter(user=instance.user, project=instance.project).delete()


@receiver(post_save, sender=ProjectContributor)
def assign_contributor_permissions(sender, instance=None, created=False, **kwargs):
    # do this only on confirmation
    if created and not instance.confirmed:
        return
    perms = []
    if instance.role == ProjectContributor.ROLE_PENTESTER:
        perms = ProjectContributor.ROLE_PENTESTER_PERMISSIONS
    elif instance.role == ProjectContributor.ROLE_READ_ONLY:
        perms = ProjectContributor.ROLE_READ_ONLY_PERMISSIONS
    for perm in perms:
        assign_perm(perm, user_or_group=instance.user, obj=instance.project)
