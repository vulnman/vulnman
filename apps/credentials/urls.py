from django.urls import path
from credentials import views


app_name = "credentials"


urlpatterns = [
	path("", views.CredentialList.as_view(), name="credentials-list")
]
