from django.urls import path
from apps.agents import views


app_name = "agents"

urlpatterns = [
    path('', views.AgentList.as_view(), name="agent-list"),
    path('create/', views.AgentCreate.as_view(), name="agent-create"),
    path('<str:pk>/delete/', views.AgentDelete.as_view(), name="agent-delete")
]
