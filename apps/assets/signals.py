from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.methodologies.models import AssetTask, Task
from apps.assets import models


@receiver(post_save, sender=models.WebApplication)
@receiver(post_save, sender=models.WebRequest)
@receiver(post_save, sender=models.Host)
def create_asset_task(sender, instance=None, created=False, **kwargs):
    # Create tasks as soon as a new asset is created
    if created:
        for task in Task.objects.filter(taskcondition__asset_type=instance.ASSET_TYPE_CHOICE[0]):                
            if instance.ASSET_TYPE_CHOICE[0] == models.WebApplication.ASSET_TYPE_CHOICE[0]:
                AssetTask.objects.create(project=instance.get_project(), task=task, asset_webapp=instance)
            elif instance.ASSET_TYPE_CHOICE[0] == models.WebRequest.ASSET_TYPE_CHOICE[0]:
                AssetTask.objects.create(project=instance.get_project(), task=task, asset_webrequest=instance)
            elif instance.ASSET_TYPE_CHOICE[0] == models.Host.ASSET_TYPE_CHOICE[0]:
                AssetTask.objects.create(project=instance.get_project(), task=task, asset_host=instance)
