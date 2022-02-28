from django.urls import path
from apps.methodologies import views


app_name = "methodology"


urlpatterns = [
    path('', views.ProjectMethodologyList.as_view(), name="project-methodology-list"),
    path('create/', views.ProjectMethodologyCreate.as_view(), name="project-methodology-create"),
    path('create-from-template/', views.ProjectMethodologyFromTemplateCreate.as_view(),
         name="project-methodology-from-template"),
    path('<str:pk>/delete/', views.ProjectMethodologyDelete.as_view(), name="project-methodology-delete"),
    path('<str:pk>/update/', views.ProjectMethodologyUpdate.as_view(), name="project-methodology-update"),
    path('<str:pk>/', views.ProjectMethodologyDetail.as_view(), name="project-methodology-detail"),
]
