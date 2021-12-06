from django.urls import path, include
from apps.projects import views


app_name = "projects"


urlpatterns = [
    path('', views.ProjectList.as_view(), name="project-list"),
    path('create/', views.ProjectCreate.as_view(), name="project-create"),

    # reporting urls
    path('reporting/', include('apps.reporting.urls')),

    # networking
    path('networking/', include('apps.networking.urls')),

    # social
    path('social/', include('apps.social.urls')),

    # vulns app
    path('vulns/', include('vulns.urls')),

    # tools
    path('tools/', include('apps.external_tools.urls')),

    # project members
    path('members/', views.ProjectMemberList.as_view(), name="project-member-list"),
    path('members/create/', views.ProjectMemberCreate.as_view(), name="project-add-member"),
    path('members/<str:pk>/delete/', views.ProjectMemberDelete.as_view(), name="project-member-delete"),

    # single project
    path('<str:pk>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('<str:pk>/update/', views.ProjectUpdate.as_view(), name="project-update"),

]
