import os
from django.conf import settings
from git import Repo


def update_vulnerability_templates():
    template_dir = os.path.join(
        settings.BASE_DIR, "resources/vulnerability_templates")
    community_templates_dir = os.path.join(template_dir, "community-vulnerability-templates")
    if os.path.isdir(community_templates_dir):
        repo = Repo(community_templates_dir)
        origin = repo.remotes.origin
        origin.pull()
    else:
        Repo.clone_from(settings.VULNERABILITY_TEMPLATE_REPO, community_templates_dir)
