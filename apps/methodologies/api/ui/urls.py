from rest_framework.routers import DefaultRouter
from apps.methodologies.api.ui import views


app_name = "methodologies"

router = DefaultRouter()

router.register("tasks", views.TaskViewSet,
                basename="task")


urlpatterns = router.urls
