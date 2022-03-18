from django.urls import path
from apps.assets import views

app_name = "assets"


urlpatterns = [
    path("webapps/", views.WebApplicationList.as_view(), name="webapp-list"),
    path("webapps/create/",views.WebApplicationCreate.as_view(), name="webapp-create"),
    path("webrequests/", views.WebRequestList.as_view(), name="webrequest-list"),
    path("webrequests/create/", views.WebRequestCreate.as_view(), name="webrequest-create"),
    path("hosts/", views.HostList.as_view(), name="host-list"),
    path("hosts/create/", views.HostCreate.as_view(), name="host-create"),
]
