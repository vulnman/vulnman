from django.urls import path
from apps.reporting import views


app_name = "reporting"


urlpatterns = [
    path('reports/', views.ReportList.as_view(), name="report-list"),
    path('reports/create/', views.ReportCreate.as_view(), name="report-create"),
    path('reports/<str:pk>/', views.ReportDetail.as_view(), name="report-detail"),
    path('reports/<str:pk>/update/', views.ReportUpdate.as_view(), name="report-update"),
    path('reports/<str:pk>/delete/', views.ReportDraftDelete.as_view(), name="report-delete")
]
