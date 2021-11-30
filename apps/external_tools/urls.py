from django.urls import path
from apps.external_tools import views


app_name = "external-tools"


urlpatterns = [
	path('import/', views.ToolImportReport.as_view(), name="tool-import")
]
