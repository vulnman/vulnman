from rest_framework.routers import DefaultRouter
from apps.findings.api.v1 import views


app_name = "findings"


router = DefaultRouter()

router.register("vulnerabilities", views.VulnerabilityViewSet, basename="vulnerability")
router.register("text-proofs", views.TextProofViewSet, basename="text-proof")

urlpatterns = router.urls
