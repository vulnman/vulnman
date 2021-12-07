from django.urls import path
from apps.social import views


app_name = "social"


urlpatterns = [
    path('employees/', views.EmployeeList.as_view(), name="employee-list"),
    path('employees/create/', views.EmployeeCreate.as_view(), name="employee-create"),
    path('employees/<str:pk>/', views.EmployeeDetail.as_view(), name="employee-detail"),

    path('credentials/', views.CredentialList.as_view(), name="credential-list"),
    path('credentials/create/', views.CredentialCreate.as_view(), name="credential-create"),
    path('credentials/<str:pk>/update/', views.CredentialUpdate.as_view(), name="credential-update")
]
