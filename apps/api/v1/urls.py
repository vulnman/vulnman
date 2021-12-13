from rest_framework.routers import DefaultRouter
from apps.networking.api.v1 import views as networking_views
from apps.projects.api.v1 import views as projects_views
from apps.findings.api.v1 import views as findings_views
from apps.methodologies.api.v1 import views as methodologies_views
from apps.agents.api.v1 import views as agent_views
from apps.commands.api.v1 import views as commands_views
from apps.social.api.v1 import views as social_views
from apps.api.swagger import swagger_urls



app_name = "v1"


router = DefaultRouter()

router.register("projects", projects_views.ProjectViewSet, basename="project")
router.register("hosts", networking_views.HostViewSet, basename="host")
router.register("services", networking_views.ServiceViewSet, basename="service")
router.register("hostnames", networking_views.HostnameViewSet, basename="hostname")
router.register("vulnerabilities/templates", findings_views.TemplateViewSet, basename="vulnerability-template")
router.register("vulnerabilities/vulns", findings_views.VulnerabilityViewSet, basename="vulnerability")
router.register("methodologies", methodologies_views.MethodologyViewSet, basename="methodology")
router.register("project-tasks", methodologies_views.ProjectTaskViewSet, basename="project-task")
router.register("commands/templates", commands_views.CommandTemplateViewSet, basename="command-template")
router.register("commands/histories", commands_views.CommandHistoryViewSet, basename="command-history")
router.register("credentials", social_views.CredentialViewSet, basename="credential")

# Agent URLs
router.register("agents/queues", agent_views.AgentQueueViewSet, basename="agent-queue")

urlpatterns = router.urls

# Add swagger docs
urlpatterns += swagger_urls
