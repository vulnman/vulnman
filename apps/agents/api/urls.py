from rest_framework.routers import DefaultRouter
from apps.agents.api.views import queue as queue_views


app_name = "agents"

router = DefaultRouter()

router.register(r'queues', queue_views.AgentQueueViewSet, basename="queue"),
router.register(r'commands', queue_views.CommandHistoryItemViewSet, basename="command")


urlpatterns = router.urls
