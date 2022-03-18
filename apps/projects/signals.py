from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.projects.models import Project, ProjectContributor
from apps.reporting.models import ReportInformation


@receiver(post_save, sender=Project)
def create_report_information(sender, instance=None, created=False, **kwargs):
    # Create tasks as soon as a new asset is created
    if created:
        ReportInformation.objects.create(project=instance)


@receiver(pre_delete, sender=ProjectContributor)
def delete_contributor_repo(sender, instance, **kwargs):
    instance.clear_perms()
