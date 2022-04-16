import os
from django.conf import settings
from git import Repo


def update_vulnerability_templates():
    template_dir = os.path.join(
        settings.BASE_DIR, "resources/vuln_templates")
    if os.path.isdir(template_dir):
        repo = Repo(template_dir)
        origin = repo.remotes.origin
        origin.pull()
    else:
        Repo.clone_from(settings.VULNERABILITY_TEMPLATE_REPO, template_dir)
