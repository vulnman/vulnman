from vulnman.settings import BASE_DIR

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'extra_views',
    'rest_framework',
    'rest_framework.authtoken',
    'crispy_forms',
    "crispy_bootstrap5",
    "guardian",
    "split_settings",
    'django_celery_results',
    "corsheaders",
    'django_filters',
    # apps
    'apps.api.apps.ApiConfig',
    'apps.account.apps.AccountConfig',
    'apps.external_tools.apps.ExternalToolsConfig',
    'apps.reporting.apps.ReportingConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.methodologies.apps.MethodologiesConfig',
    'apps.findings.apps.FindingsConfig',
    'apps.assets.apps.AssetsConfig',
]
