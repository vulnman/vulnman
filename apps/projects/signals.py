from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from guardian.shortcuts import get_perms, remove_perm
from apps.projects.models import Project, ProjectContributor, ProjectAPIToken
#from apps.reporting.models import ReportConfiguration


#@receiver(post_save, sender=Project)
#def create_report_information(sender, instance=None, created=False, **kwargs):
#    # Create tasks as soon as a new asset is created
#    if created:
#        ReportConfiguration.objects.create(project=instance)


@receiver(pre_delete, sender=ProjectContributor)
def delete_contributor_from_project(sender, instance, **kwargs):
    perms = get_perms(instance.user, instance.project)
    for perm in perms:
        remove_perm(perm, user_or_group=instance.user, obj=instance.project)
    # ensure that the API tokens are wiped, when a contributor is deleted
    # otherwise the contributor may still have access to the project
    ProjectAPIToken.objects.filter(user=instance.user, project=instance.project).delete()
