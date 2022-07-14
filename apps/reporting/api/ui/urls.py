from rest_framework.routers import DefaultRouter
from apps.reporting.api.ui import views


app_name = "reporting"


router = DefaultRouter()

router.register("task-results", views.TaskResultViewSet, basename="task-result")


urlpatterns = router.urls
