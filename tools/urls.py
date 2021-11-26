from django.urls import path
from tools import views


app_name = "tools"


urlpatterns = [
	path('import/', views.ToolImportReport.as_view(), name="tool-import")
]
