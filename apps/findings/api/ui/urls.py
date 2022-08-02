from rest_framework.routers import DefaultRouter
from apps.findings.api.ui import views


app_name = "findings"

router = DefaultRouter()

router.register("templates", views.TemplateViewSet,
                basename="template")
router.register("proofs", views.ProofViewSet, basename="proof")


urlpatterns = router.urls
