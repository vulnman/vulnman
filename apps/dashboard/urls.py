from django.urls import path
from apps.dashboard import views

app_name = "dashboard"


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('dashboard/', views.Dashboard.as_view(), name="dashboard")
]
