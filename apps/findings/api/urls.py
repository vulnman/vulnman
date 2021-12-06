from rest_framework.routers import DefaultRouter
from apps.findings.api import views


app_name = "findings"


router = DefaultRouter()
router.register(r'templates', views.TemplateViewSet, basename="template")


urlpatterns = router.urls
