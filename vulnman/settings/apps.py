from vulnman.settings import BASE_DIR

# Application definition

INSTALLED_APPS = [
    # keep before django.contrib.admin
    'dal',
    'dal_select2',
    'queryset_sequence',
    'dal_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django_tex',
    'extra_views',
    'rest_framework',
    'dry_rest_permissions',
    'crispy_forms',
    "crispy_bootstrap5",
    "guardian",
    "taggit",
    "split_settings",
    # apps
    'apps.api.apps.ApiConfig',
    'apps.account.apps.AccountConfig',
    'apps.external_tools.apps.ExternalToolsConfig',
    'apps.reporting.apps.ReportingConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.networking.apps.NetworkingConfig',
    'apps.methodologies.apps.MethodologiesConfig',
    'apps.social.apps.SocialConfig',
    'apps.findings.apps.FindingsConfig',
    'apps.agents.apps.AgentsConfig',
    'apps.commands.apps.CommandsConfig',
    'apps.tagging.apps.TaggingConfig',
    'apps.assets.apps.AssetsConfig',
]
