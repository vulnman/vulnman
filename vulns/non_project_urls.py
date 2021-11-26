from django.urls import path
from vulns import views


app_name = "vulns"

urlpatterns = [
    path('', views.VulnerabilityTemplateList.as_view(), name="vuln-template-list"),
    path('create/', views.VulnerabilityTemplateCreate.as_view(), name="vuln-template-create"),
    path('autocomplete/', views.VulnerabilityTemplateAutocomplete.as_view(), name="vuln-template-autocomplete"),
    path('<str:pk>/', views.VulnerabilityTemplateDetail.as_view(), name="vuln-template-detail")
]
