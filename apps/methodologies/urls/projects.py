from django.urls import path
from apps.methodologies import views


app_name = "methodologies"


urlpatterns = [
    path("todos/", views.ProjectTaskList.as_view(), name="project-task-list"),
    path("todos/<str:pk>/", views.ProjectTaskDetail.as_view(), name="project-task-detail"),
    path("todos/<str:pk>/status-update/", views.ProjectTaskStatusUpdate.as_view(), name="project-task-status-update")
]
