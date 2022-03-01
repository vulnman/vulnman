from django.urls import path
from apps.account.api.v1 import views


urlpatterns = [
    path("", views.CustomAuthToken.as_view(), name="api-token-auth")
]
