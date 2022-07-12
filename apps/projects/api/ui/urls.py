from rest_framework.routers import DefaultRouter
from apps.projects.api.ui import views

app_name = "projects"

router = DefaultRouter()

router.register("", views.ProjectViewSet, basename="project")

urlpatterns = router.urls
