from django.urls import path
from apps.reporting import views


app_name = "reporting"


urlpatterns = [
    path('reports/', views.ReportList.as_view(), name="report-list"),
    path('reports/draft-create', views.PentestReportDraftCreate.as_view(), name="report-draft-create"),
    path('reports/<str:pk>/download/', views.PentestReportDownload.as_view(), name="report-download"),
    path('reports/<str:pk>/share/', views.ReportSharedTokenCreate.as_view(), name="report-share"),
    path('reports/<str:pk>/<str:token>/', views.ReportSharedDetail.as_view(), name="report-shared-report-detail")
]
