from django.urls import path, include
from apps.projects import views


app_name = "projects"


urlpatterns = [
    path('', views.ProjectList.as_view(), name="project-list"),
    path('create/', views.ProjectCreate.as_view(), name="project-create"),

    # reporting urls
    path('reporting/', include('apps.reporting.urls')),

    # vulns app
    path('vulns/', include('vulns.urls')),

    # tools
    path('tools/', include('apps.external_tools.urls')),

    # single project
    path('<str:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('<str:pk>/update/', views.ProjectUpdate.as_view(), name="project-update"),

]
