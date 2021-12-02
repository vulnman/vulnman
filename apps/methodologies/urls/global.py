from django.urls import path
from apps.methodologies import views


app_name = "methodology"


urlpatterns = [
    path("", views.MethodologyList.as_view(), name="methodology-list"),
    path("create/", views.MethodologyCreate.as_view(), name="methodology-create"),
    path("<str:pk>/", views.MethodologyDetail.as_view(), name="methodology-detail"),
    path("<str:pk>/update/", views.MethodologyUpdate.as_view(), name="methodology-update"),
    path("<str:pk>/delete/", views.MethodologyDelete.as_view(), name="methodology-delete"),
    path("commands/<str:pk>/update/", views.SuggestedCommandUpdate.as_view(), name="suggested-command-update"),
]
