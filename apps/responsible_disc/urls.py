from django.urls import path
from apps.responsible_disc import views


app_name = "responsible_disc"


urlpatterns = [
    path("", views.VulnerabilityList.as_view(), name="vulnerability-list"),
    path("create/", views.VulnerabilityCreate.as_view(), name="vulnerability-create"),
    path("<str:pk>/", views.VulnerabilityDetail.as_view(), name="vulnerability-detail"),
    path("<str:pk>/update/", views.VulnUpdate.as_view(), name="vulnerability-update"),
    path("<str:pk>/delete/", views.VulnDelete.as_view(), name="vulnerability-delete"),

    path('vulnerabilities/<str:pk>/add-text-proof/', views.AddTextProof.as_view(),
         name="vulnerability-add-text-proof"),
    path('vulnerabilities/<str:pk>/add-image-proof/', views.AddImageProof.as_view(),
         name="vulnerability-add-image-proof"),
    path('vulnerabilities/<str:pk>/export-pdf/', views.VulnerabilityExport.as_view(), name="vulnerability-export-pdf"),
    path('vulnerabilities/<str:pk>/export-advisory/', views.VulnerabilityAdvisoryExport.as_view(),
         name="vulnerability-export-advisory"),
    path('vulnerabilities/<str:pk>/notify-vendor/',
         views.VulnerabilityNotifyVendor.as_view(), name="vulnerability-notify-vendor"),
    path('vulnerabilities/<int:pk>/add-log-item/', views.VulnerabilityLogCreate.as_view(),
         name="vulnerability-log-create"),

    path('proofs/text/<int:pk>/delete/', views.TextProofDelete.as_view(), name="text-proof-delete"),
    path('proofs/text/<int:pk>/update/', views.TextProofUpdate.as_view(), name="text-proof-update"),
    path('proofs/image/<int:pk>/delete/', views.ImageProofDelete.as_view(), name="image-proof-delete"),
    path('proofs/image/<int:pk>/update/', views.ImageProofUpdate.as_view(), name="image-proof-update")
]
