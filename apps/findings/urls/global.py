from django.urls import path
from apps.findings import views


app_name = "findings"


urlpatterns = [
    path('', views.TemplateList.as_view(), name="template-list"),
    path('<str:pk>/', views.TemplateDetail.as_view(), name="template-detail")
]
