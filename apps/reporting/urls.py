from django.urls import path
from apps.reporting import views


app_name = "reporting"


urlpatterns = [
    path('reports/', views.ReportList.as_view(), name="report-list"),
    path('reports/create/', views.ReportCreate.as_view(), name="report-create"),
    path('reports/draft-create', views.PentestReportDraftCreate.as_view(), name="report-draft-create"),
    path('reports/<str:pk>/download/', views.PentestReportDownload.as_view(), name="report-download"),
    path('reports/<str:pk>/', views.ReportDetail.as_view(), name="report-detail"),
    path('reports/<str:pk>/update/', views.ReportUpdate.as_view(), name="report-update"),
    path('reports/<str:pk>/delete/', views.ReportDraftDelete.as_view(), name="report-delete"),
    path('reports/<str:pk>/share/', views.ReportSharedTokenCreate.as_view(), name="report-share"),
    path('reports/<str:pk>/<str:token>/', views.ReportSharedDetail.as_view(), name="report-shared-report-detail")
]
