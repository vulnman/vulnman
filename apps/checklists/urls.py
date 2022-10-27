from django.urls import path
from . import views


app_name = "checklists"


urlpatterns = [
    path('', views.ProjectChecklistList.as_view(), name="checklists-list"),
    path('create/', views.ProjectChecklistCreate.as_view(), name="checklists-create"),
]
