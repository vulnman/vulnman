from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1 import viewsets


app_name = "v1"


router = DefaultRouter()

router.register(
    "vulnerabilities/proofs", viewsets.ProofViewSet,
    basename="vulnerability-proof")

router.register(
    "reports", viewsets.reports.ReportViewSet, basename="report")

router.register(
    "reports/tasks", viewsets.reports.ReportTaskResultViewSet,
    basename="report-task-result")


urlpatterns = router.urls


urlpatterns += [
    path("agents/", include("api.v1.urls.agents"))
]
