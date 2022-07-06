from django.urls import path, include

app_name = "api"


urlpatterns = [
    path("ui/", include("api.ui.urls")),
    path("v1/", include("api.v1.urls", namespace="v1")),
]
