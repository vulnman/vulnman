from django.urls import path
from apps.findings import views


app_name = "findings"


urlpatterns = [
    path("vulnerabilities/", views.VulnList.as_view(), name="vulnerability-list"),
    path('vulnerabilities/create/', views.VulnCreate.as_view(), name="vulnerability-create"),
    path('vulnerabilities/<str:pk>/', views.VulnDetail.as_view(), name="vulnerability-detail"),
    path('vulnerabilities/<str:pk>/delete/', views.VulnDelete.as_view(), name="vulnerability-delete"),
    path('vulnerabilities/<str:pk>/update/', views.VulnUpdate.as_view(), name="vulnerability-update"),

]
