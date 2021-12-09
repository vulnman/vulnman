from django.urls import path, include

app_name = "api"

urlpatterns = [
    # path('vulns/', include('vulns.api.urls')),
    #path('methodologies/', include('apps.methodologies.api.urls')),
    # path('findings/', include('apps.findings.api.urls')),
    # path('agents/', include('apps.agents.api.urls')),
]

urlpatterns += [
    path("v1/", include("apps.api.v1.urls", namespace="v1")),
]
