from rest_framework.routers import DefaultRouter
from apps.assets.api.v1 import views as assets_views
from apps.projects.api.v1 import views as projects_views
from apps.findings.api.v1 import views as findings_views
from apps.reporting.api.v1 import views as reporting_views
from apps.methodologies.api.v1 import views as methodologies_views
#from apps.agents.api.v1 import views as agent_views
#from apps.commands.api.v1 import views as commands_views


app_name = "v1"


router = DefaultRouter()

router.register("projects", projects_views.ProjectViewSet, basename="project")
router.register("user-accounts", findings_views.UserAccountViewSet, basename="user-account")
router.register("vulnerabilities/text-proof", findings_views.TextProofViewSet, basename="text-proof")
router.register("vulnerabilities/image-proofs", findings_views.ProofViewSet, basename="proof")
router.register("vulnerabilities", findings_views.VulnerabilityViewSet, basename="vulnerability")
router.register("tasks/assets", methodologies_views.AssetTaskViewSet, basename="asset-task")
router.register("tasks", methodologies_views.TaskViewSet, basename="task")

urlpatterns = router.urls
