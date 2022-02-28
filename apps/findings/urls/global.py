from django.urls import path
from apps.findings import views


app_name = "findings"


urlpatterns = [
    path('', views.TemplateList.as_view(), name="template-list"),
    path('create/', views.TemplateCreate.as_view(), name="template-create"),
    path('autocomplete/', views.VulnerabilityTemplateAutocomplete.as_view(), name="template-autocomplete"),
    path('<str:pk>/', views.TemplateDetail.as_view(), name="template-detail"),
    path('<str:pk>/update/', views.TemplateUpdate.as_view(), name="template-update")
]
