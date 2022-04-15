from django.urls import path, include
from apps.projects import views


app_name = "projects"


urlpatterns = [
    path('', views.ProjectList.as_view(), name="project-list"),
    path('create/', views.ProjectCreate.as_view(), name="project-create"),

    # reporting urls
    path('reporting/', include('apps.reporting.urls')),

    # networking
    # path('networking/', include('apps.networking.urls')),

    # command
    path('methodologies/', include('apps.methodologies.urls.projects')),

    # findings
    path('findings/', include('apps.findings.urls.projects')),

    path('assets/', include('apps.assets.urls')),

    path('tokens/', views.ProjectTokenList.as_view(), name="token-list"),
    path('tokens/create/', views.ProjectTokenCreate.as_view(), name="token-create"),
    path('tokens/<str:pk>/delete/', views.ProjectTokenDelete.as_view(), name="token-delete"),

    # single project
    path('<str:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('<str:pk>/update/', views.ProjectUpdate.as_view(), name="project-update"),
    path('<str:pk>/close/', views.ProjectUpdateClose.as_view(), name="project-close"),
    path('<str:pk>/contributors/', views.ProjectContributorList.as_view(), name="contributor-list"),
]
