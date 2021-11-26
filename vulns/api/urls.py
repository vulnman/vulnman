from rest_framework.routers import DefaultRouter
from vulns.api import views

app_name = "vulns"

router = DefaultRouter()
router.register(r'vulnerability-templates', views.VulnerabilityTemplateViewSet, basename="vulnerability-template")


urlpatterns = router.urls
