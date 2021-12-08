from rest_framework.routers import DefaultRouter
from apps.api.v1 import views
from apps.agents.api.views import queue as queue_views

app_name = "v1"


router = DefaultRouter()

router.register('agents/queues', queue_views.AgentQueueViewSet, basename="queue"),
router.register('agents/commands', queue_views.CommandHistoryItemViewSet, basename="command")


urlpatterns = router.urls
