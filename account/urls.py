from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('profile/edit/', views.ProfileEdit.as_view(), name="profile-edit")
]
