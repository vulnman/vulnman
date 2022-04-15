from rest_framework.routers import DefaultRouter
from api.v1 import viewsets


app_name = "agents"


router = DefaultRouter()

router.register(
    "hosts", viewsets.assets.AgentHostViewSet, basename="host")

router.register(
    "services", viewsets.assets.AgentServiceViewSet, basename="service")

router.register(
    "vulnerabilities", viewsets.vulnerability.AgentVulnerabilityViewSet,
    basename="vulnerability")

router.register(
    "text-proofs", viewsets.vulnerability.AgentTextProofViewSet,
    basename="text-proof")


urlpatterns = router.urls
