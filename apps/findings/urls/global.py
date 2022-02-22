from django.urls import path
from apps.findings import views


app_name = "findings"


urlpatterns = [
    path('', views.TemplateList.as_view(), name="template-list"),
    path('autocomplete/', views.VulnerabilityTemplateAutocomplete.as_view(), name="template-autocomplete"),
]
