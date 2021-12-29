from django.urls import path
from apps.projects import views


app_name = "clients"

urlpatterns = [
    path("", views.ClientList.as_view(), name="client-list"),
    path("create/", views.ClientCreate.as_view(), name="client-create"),
    path("<str:pk>/", views.ClientDetail.as_view(), name="client-detail")
]
