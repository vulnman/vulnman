from django.urls import path
from apps.methodologies import views


app_name = "methodology"


urlpatterns = [
    path("", views.TaskList.as_view(), name="methodology-list"),
]
