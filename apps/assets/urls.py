from django.urls import path
from apps.assets import views

app_name = "assets"


urlpatterns = [
    path("webapps/", views.WebApplicationList.as_view(), name="webapp-list"),
    path("webapps/create/",views.WebApplicationCreate.as_view(), name="webapp-create"),
    path("webapps/<str:pk>/update/", views.WebApplicationUpdate.as_view(), name="webapp-update"),
    path("webrequests/", views.WebRequestList.as_view(), name="webrequest-list"),
    path("webrequests/create/", views.WebRequestCreate.as_view(), name="webrequest-create"),
    path("hosts/", views.HostList.as_view(), name="host-list"),
    path("hosts/create/", views.HostCreate.as_view(), name="host-create"),
    path("services/", views.ServiceList.as_view(), name="service-list"),
    path("services/create/", views.ServiceCreate.as_view(), name="service-create"),
]
