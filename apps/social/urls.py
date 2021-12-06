from django.urls import path
from apps.social import views


app_name = "social"


urlpatterns = [
    path('employees/', views.EmployeeList.as_view(), name="employee-list"),
    path('employees/<str:pk>/', views.EmployeeDetail.as_view(), name="employee-detail")
]
