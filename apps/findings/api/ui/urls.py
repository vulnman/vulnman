from rest_framework.routers import DefaultRouter
from apps.findings.api.ui import views


app_name = "findings"

router = DefaultRouter()

router.register("templates", views.TemplateViewSet,
                basename="template")


urlpatterns = router.urls
