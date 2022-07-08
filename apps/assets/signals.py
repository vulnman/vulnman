from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.assets import models
from apps.methodologies.models import AssetTask, Task


@receiver(post_save, sender=models.Service)
@receiver(post_save, sender=models.WebApplication)
def create_webapp_task(sender, instance=None, created=False, **kwargs):
    # TODO: write tests
    # Create tasks as soon as a new asset is created
    if created:
        task_qs = Task.objects.filter(
            taskcondition__asset_type=instance.ASSET_TYPE_CHOICE[0]).distinct()
        for task in task_qs:
            conditions = task.taskcondition_set.all()
            for condition in conditions:
                d = {
                    condition.name: condition.condition,
                    "pk": instance.pk}
                create_data = {
                    "project": instance.get_project(), "task": task}
                if condition.asset_type == models.WebApplication.ASSET_TYPE_CHOICE[0]:
                    create_data["asset_webapp"] = instance
                    if condition.name == "always":
                        AssetTask.objects.create(**create_data)
                        break
                    if models.WebApplication.objects.filter(**d).exists():
                        AssetTask.objects.create(**create_data)
                        break
                elif condition.asset_type == models.Service.ASSET_TYPE_CHOICE[0]:
                    create_data["asset_service"] = instance
                    if condition.name == "always":
                        AssetTask.objects.create(**create_data)
                        break
                    if models.Service.objects.filter(**d).exists():
                        AssetTask.objects.create(**create_data)
                        break
