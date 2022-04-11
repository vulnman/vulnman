from django.urls import path
from apps.reporting import views


app_name = "reporting"


urlpatterns = [
    path('reports/', views.ReportList.as_view(), name="report-list"),
    path('reports/draft-create', views.PentestReportDraftCreate.as_view(), name="report-draft-create"),
    path('reports/create/', views.PentestReportCreate.as_view(), name="report-create"),
    path('reports/<str:pk>/download/', views.PentestReportDownload.as_view(), name="report-download"),
    path('reports/<str:pk>/delete/', views.PentestReportDelete.as_view(), name="report-delete"),
]
