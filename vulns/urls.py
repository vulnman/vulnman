from django.urls import path
from vulns import views


app_name = "vulns"

urlpatterns = [
    path('', views.VulnList.as_view(), name="vuln-list"),
    path('create/', views.VulnCreate.as_view(), name="vuln-create"),
    path('hosts/', views.HostList.as_view(), name="host-list"),
    path('hosts/create/', views.HostCreate.as_view(), name="host-create"),
    path('hosts/<str:pk>/', views.HostDetail.as_view(), name="host-detail"),

    path('<str:pk>/', views.VulnDetail.as_view(), name="vuln-detail"),
    path('<str:pk>/delete/', views.VulnDelete.as_view(), name="vuln-delete"),
    path('<str:pk>/update/', views.VulnUpdate.as_view(), name="vuln-update"),
]
