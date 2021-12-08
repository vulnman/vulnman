from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


app_name = "api"


schema_view = get_schema_view(
   openapi.Info(
      title="Vulnman API",
      default_version='v1',
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('vulns/', include('vulns.api.urls')),
    path('projects/', include('apps.projects.api.urls')),
    path('networking/', include('apps.networking.api.urls')),
    path('methodologies/', include('apps.methodologies.api.urls')),
    path('findings/', include('apps.findings.api.urls')),
    path('agents/', include('apps.agents.api.urls')),
]

urlpatterns += [
    path('v1/', include('apps.api.v1.urls'))
]

