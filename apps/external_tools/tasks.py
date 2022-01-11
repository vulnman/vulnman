from celery import shared_task
from django.conf import settings
from django.utils.module_loading import import_string
from apps.projects.models import Project
from django.contrib.auth.models import User


@shared_task
def do_import_report(plugin_name, data, project, user):
    tool_module = import_string(settings.EXTERNAL_TOOLS[plugin_name])
    plugin = tool_module()
    return plugin.parse(data, Project.objects.get(pk=project), User.objects.get(pk=user))
