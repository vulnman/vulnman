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
    path('vulnerabilities/<str:pk>/add-text-proof/', views.AddTextProof.as_view(), name="vulnerability-add-text-proof"),
    path('vulnerabilities/<str:pk>/add-image-proof/', views.AddImageProof.as_view(), name="vulnerability-add-image-proof"),
    path('proofs/ordering/', views.ProofSetOrder.as_view(), name="proof-set-order"),
    path('user-accounts/', views.UserAccountList.as_view(), name="user-account-list"),
    path('user-accounts/create/', views.UserAccountCreate.as_view(), name="user-account-create"),
]
