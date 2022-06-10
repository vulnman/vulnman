from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1 import viewsets


app_name = "v1"


router = DefaultRouter()

router.register(
    "projects", viewsets.projects.ProjectViewSet,
    basename="project")


router.register(
    "hosts", viewsets.HostViewSet, basename="host"
)

router.register(
    "services", viewsets.ServiceViewSet, basename="service")

router.register(
    "webapplications", viewsets.WebApplicationViewSet,
    basename="webapplication")

router.register(
    "webrequests", viewsets.WebRequestViewSet, basename="webrequest")

router.register(
    "tasks", viewsets.TaskViewSet, basename="task")

router.register(
    "vulnerabilities/templates", viewsets.templates.TemplateViewSet,
    basename="vulnerability-template")

router.register(
    "vulnerabilities/proofs", viewsets.ProofViewSet,
    basename="vulnerability-proof")

router.register(
    "reports", viewsets.reports.ReportViewSet, basename="report")

router.register(
    "reports/tasks", viewsets.reports.ReportTaskResultViewSet,
    basename="report-task-result")

router.register(
    "report-information", viewsets.reports.ReportInformationViewSet,
    basename="report-information")

router.register(
    "responsible-disclosure/proofs", viewsets.responsible_disc.ProofViewSet,
    basename="responsible-disc-proof"
)


urlpatterns = router.urls


urlpatterns += [
    path("agents/", include("api.v1.urls.agents"))
]
