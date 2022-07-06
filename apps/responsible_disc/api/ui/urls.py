from rest_framework.routers import DefaultRouter
from apps.responsible_disc.api.ui import views


app_name = "responsible-disclosure"

router = DefaultRouter()

router.register("proofs", views.OrderProofViewSet,
                basename="proof")


urlpatterns = router.urls
