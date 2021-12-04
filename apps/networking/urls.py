from django.urls import path
from apps.networking import views


app_name = "networking"


urlpatterns = [

    # hosts
    path('hosts/', views.HostList.as_view(), name="host-list"),
    path('hosts/create/', views.HostCreate.as_view(), name="host-create"),
    path('hosts/<str:pk>/', views.HostDetail.as_view(), name="host-detail"),
    path('hosts/<str:pk>/edit/', views.HostEdit.as_view(), name="host-edit"),
    path('hosts/<str:pk>/delete/', views.HostDelete.as_view(), name="host-delete"),

]
