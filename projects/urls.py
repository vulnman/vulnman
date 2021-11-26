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

    path('<str:project_pk>/vulns/', include('vulns.urls')),
    path('<str:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('<str:pk>/update/', views.ProjectUpdate.as_view(), name="project-update"),
    path('<str:project_pk>/reports/<str:pk>/update/', views.ReportUpdate.as_view(), name="report-update"),

    # credentials
    path('<str:project_pk>/credentials/', include('credentials.urls')),

    # tools
    path('<str:project_pk>/tools/', include('tools.urls'))
]
