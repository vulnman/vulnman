from django.urls import path, include

app_name = "api"


urlpatterns = [
    path("v1/", include("apps.api.v1.urls", namespace="v1")),
]
