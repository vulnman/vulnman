from rest_framework.routers import DefaultRouter
from apps.api.v2 import viewsets


app_name = "v2"


router = DefaultRouter()

router.register(
    "services", viewsets.assets.ServiceViewSet, basename="service")

router.register(
    "hosts", viewsets.assets.HostViewSet, basename="host")

router.register(
    "vulnerabilities", viewsets.vulnerability.VulnerabilityViewSet,
    basename="vulnerability")

router.register(
    "text-proofs", viewsets.proof.TextProofViewSet, basename="text-proof")


urlpatterns = router.urls
