from django.urls import path, include


app_name = "api"

urlpatterns = [
    path('vulns/', include('vulns.api.urls'))
]
