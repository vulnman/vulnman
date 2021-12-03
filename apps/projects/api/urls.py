from rest_framework.routers import DefaultRouter
from apps.projects.api import views

app_name = "projects"

router = DefaultRouter()
router.register(r'', views.ProjectViewSet, basename="project")

urlpatterns = router.urls
