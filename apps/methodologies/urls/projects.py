from django.urls import path
from core.views import tasks as views


app_name = "methodologies"


urlpatterns = [
    path("todos/", views.ProjectTaskList.as_view(), name="project-task-list"),
    path("todos/<str:pk>/", views.ProjectTaskDetail.as_view(), name="project-task-detail"),
    path("todos/<str:pk>/status-update/", views.ProjectTaskStatusUpdate.as_view(), name="project-task-status-update")
]
