from rest_framework.routers import DefaultRouter
from apps.assets.api.ui import views


app_name = "assets"

router = DefaultRouter()

router.register("hosts", views.HostViewSet, basename="host")
router.register("services", views.ServiceViewSet, basename="service")
router.register("web-applications", views.WebApplicationViewSet, basename="web-application")


urlpatterns = router.urls
