from django.urls import path
from apps.account import views

app_name = "account"

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('profile/update/', views.ProfileUpdate.as_view(), name="profile-update"),
    path('profile/2fa/setup/', views.Setup2FAView.as_view(), name="setup-2fa"),
    path('profile/2fa/setup/qr/', views.QRCodeGeneratorView.as_view(), name="setup-2fa-qr"),
    path('profile/2fa/disable/', views.Disable2FAView.as_view(), name="disable-2fa"),
    path('profile/<str:slug>/', views.Profile.as_view(), name="user-profile"),
    path('change-password/', views.ChangePassword.as_view(), name="change-password"),

    path('activate/<str:uidb64>/<str:token>/', views.ActivateAccount.as_view(), name="activate-account")
]
