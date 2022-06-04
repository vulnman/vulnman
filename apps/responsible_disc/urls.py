from django.urls import path
from apps.responsible_disc import views


app_name = "responsible_disc"


urlpatterns = [
    path("", views.VulnerabilityList.as_view(), name="vulnerability-list"),
    path("create/", views.VulnerabilityCreate.as_view(), name="vulnerability-create")
]
