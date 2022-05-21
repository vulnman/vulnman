from django.urls import path
from apps.findings import views


app_name = "findings"


urlpatterns = [
    path("vulnerabilities/", views.VulnList.as_view(), name="vulnerability-list"),
    path('vulnerabilities/create/', views.VulnCreate.as_view(), name="vulnerability-create"),
    path('vulnerabilities/proofs/text/delete/', views.TextProofDelete.as_view(), name="proof-delete"),
    path('vulnerabilities/<str:pk>/', views.VulnDetail.as_view(), name="vulnerability-detail"),
    path('vulnerabilities/<str:pk>/delete/', views.VulnDelete.as_view(), name="vulnerability-delete"),
    path('vulnerabilities/<str:pk>/update/', views.VulnUpdate.as_view(), name="vulnerability-update"),
    path('vulnerabilities/<str:pk>/update-cvss/', views.VulnerabilityCVSSUpdate.as_view(), name="vulnerability-cvss-update"),
    path('vulnerabilities/<str:pk>/add-text-proof/', views.AddTextProof.as_view(), name="vulnerability-add-text-proof"),
    path('vulnerabilities/<str:pk>/update-text-proof/', views.TextProofUpdate.as_view(), name="text-proof-update"),
    path('vulnerabilities/<str:pk>/add-image-proof/', views.AddImageProof.as_view(), name="vulnerability-add-image-proof"),
    path('vulnerabilities/<str:pk>/image-text-proof/', views.ImageProofUpdate.as_view(), name="image-proof-update"),
    path('image-proof/<str:pk>/delete/', views.ImageProofDelete.as_view(), name="image-proof-delete"),
    path('text-proof/<str:pk>/delete/', views.TextProofDelete.as_view(), name="text-proof-delete"),
    # path('proofs/ordering/', views.ProofSetOrder.as_view(), name="proof-set-order"),
    path('user-accounts/', views.UserAccountList.as_view(), name="user-account-list"),
    path('user-accounts/create/', views.UserAccountCreate.as_view(), name="user-account-create"),
    path('user-accounts/<str:pk>/delete/', views.UserAccountDelete.as_view(), name="user-account-delete")
]
