from rest_framework.routers import DefaultRouter
from apps.assets.api.v1 import views


app_name = "assets"


router = DefaultRouter()

router.register("hosts", views.HostViewSet, basename="host")
router.register("services", views.ServiceViewSet, basename="service")

urlpatterns = router.urls
