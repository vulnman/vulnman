from django.urls import path, include
from projects import views


app_name = "projects"


urlpatterns = [
    path('', views.ProjectList.as_view(), name="project-list"),
    path('create/', views.ProjectCreate.as_view(), name="project-create"),

    # reporting urls
    path('reports/', views.ReportList.as_view(), name="report-list"),
    path('reports/create/', views.ReportCreate.as_view(), name="report-create"),
    path('reports/<str:pk>/', views.ReportDetail.as_view(), name="report-detail"),
    path('reports/<str:pk>/update/', views.ReportUpdate.as_view(), name="report-update"),

    # vulns app
    path('vulns/', include('vulns.urls')),

    # credentials
    path('credentials/', include('credentials.urls')),

    # tools
    path('tools/', include('tools.urls')),

    # single project
    path('<str:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('<str:pk>/update/', views.ProjectUpdate.as_view(), name="project-update"),

]
