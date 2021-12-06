from rest_framework.routers import DefaultRouter
from apps.methodologies.api import views

app_name = "methodologies"

router = DefaultRouter()
router.register(r'', views.MethodologyViewSet, basename="methodology"),

urlpatterns = router.urls
