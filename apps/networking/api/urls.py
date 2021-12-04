from rest_framework.routers import DefaultRouter
from apps.networking.api import views

app_name = "networking"

router = DefaultRouter()
router.register(r'hosts', views.HostViewSet, basename="host")

urlpatterns = router.urls
