from django.urls import path, include


app_name = "v1"


urlpatterns = [
    path("assets/", include("apps.assets.api.v1.urls")),
    path("vulnerabilities", include("apps.findings.api.v1.urls"))
]
