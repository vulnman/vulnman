from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1 import viewsets


app_name = "v1"


router = DefaultRouter()

router.register(
    "projects", viewsets.projects.ProjectViewSet,
    basename="project")

router.register(
    "vulnerabilities/templates", viewsets.templates.TemplateViewSet,
    basename="vulnerability-template")

router.register(
    "vulnerabilities/proofs", viewsets.vulnerability.ProofViewSet,
    basename="vulnerability-proof")

router.register(
    "reports", viewsets.reports.ReportViewSet, basename="report")

router.register(
    "reports/tasks", viewsets.reports.ReportTaskResultViewSet,
    basename="report-task-result")

router.register(
    "report-information", viewsets.reports.ReportInformationViewSet,
    basename="report-information")


urlpatterns = router.urls


urlpatterns += [
    path("agents/", include("api.v1.urls.agents"))
]
