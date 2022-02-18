from django.urls import path
from apps.assets import views

app_name = "assets"


urlpatterns = [
    path("webapps/", views.WebApplicationList.as_view(), name="webapp-list"),
    path("webapps/create/",views.WebApplicationCreate.as_view(), name="webapp-create")
]
