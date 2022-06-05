from django.urls import path
from apps.responsible_disc import views


app_name = "responsible_disc"


urlpatterns = [
    path("", views.VulnerabilityList.as_view(), name="vulnerability-list"),
    path("create/", views.VulnerabilityCreate.as_view(), name="vulnerability-create"),
    path("<str:pk>/", views.VulnerabilityDetail.as_view(), name="vulnerability-detail"),
    path('vulnerabilities/<str:pk>/add-text-proof/', views.AddTextProof.as_view(),
         name="vulnerability-add-text-proof"),
    path('vulnerabilities/<str:pk>/add-image-proof/', views.AddImageProof.as_view(),
         name="vulnerability-add-image-proof"),

    path('proofs/text/<str:pk>/delete/', views.TextProofDelete.as_view(), name="text-proof-delete"),
    path('proofs/image/<str:pk>/delete/', views.ImageProofDelete.as_view(), name="image-proof-delete"),
]
