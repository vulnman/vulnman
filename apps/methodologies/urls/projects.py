from django.urls import path
from apps.methodologies import views


app_name = "methodologies"


urlpatterns = [
    path("todos/", views.ProjectToDos.as_view(), name="project-todos-list"),
]
