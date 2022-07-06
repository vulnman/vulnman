from django.urls import path, include


app_name = "ui"


urlpatterns = [
    path("responsible-disclosure/", include('apps.responsible_disc.api.ui.urls')),
    path("methodologies/", include('apps.methodologies.api.ui.urls')),
    path("findings/", include('apps.findings.api.ui.urls'))
]

