from rest_framework.routers import DefaultRouter
from apps.assets.api.v1 import views as assets_views
from apps.projects.api.v1 import views as projects_views
from apps.findings.api.v1 import views as findings_views
from apps.reporting.api.v1 import views as reporting_views
#from apps.findings.api.v1 import views as findings_views
from apps.methodologies.api.v1 import views as methodologies_views
#from apps.agents.api.v1 import views as agent_views
#from apps.commands.api.v1 import views as commands_views


app_name = "v1"


router = DefaultRouter()

router.register("projects/contributors", projects_views.ProjectContributorViewSet, basename="project-contributor")
router.register("projects", projects_views.ProjectViewSet, basename="project")
router.register("user-accounts", findings_views.UserAccountViewSet, basename="user-account")
router.register("vulnerabilities/templates", findings_views.TemplateViewSet, basename="vulnerability-template")
router.register("vulnerabilities/proofs", findings_views.ProofViewSet, basename="proof")
router.register("vulnerabilities", findings_views.VulnerabilityViewSet, basename="vulnerability")
router.register("reports", reporting_views.ReportViewSet, basename="report")
router.register("report-information", reporting_views.ReportInformationViewSet, basename="report-information")
router.register("reports/tasks", reporting_views.ReportTaskResult, basename="report-task-result")
router.register("tasks/assets", methodologies_views.AssetTaskViewSet, basename="asset-task")
router.register("tasks", methodologies_views.TaskViewSet, basename="task")
router.register("assets/webapplications", assets_views.WebApplicationViewSet, basename="webapplication")
router.register("assets/webrequests", assets_views.WebRequestViewSet, basename="webrequest")
router.register("assets/hosts", assets_views.HostViewSet, basename="host")
#router.register("commands/templates", commands_views.CommandTemplateViewSet, basename="command-template")
#router.register("commands/histories", commands_views.CommandHistoryViewSet, basename="command-history")
#router.register("credentials", social_views.CredentialViewSet, basename="credential")

# Agent URLs
#router.register("agents/queues", agent_views.AgentQueueViewSet, basename="agent-queue")

urlpatterns = router.urls
