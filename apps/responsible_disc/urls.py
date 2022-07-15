from django.urls import path
from apps.responsible_disc import views


app_name = "responsible_disc"


urlpatterns = [
    path("", views.VulnerabilityList.as_view(), name="vulnerability-list"),
    path("create/", views.VulnerabilityCreate.as_view(), name="vulnerability-create"),
    path("<str:pk>/", views.VulnerabilityDetail.as_view(), name="vulnerability-detail"),
    path("<str:pk>/update/", views.VulnUpdate.as_view(), name="vulnerability-update"),
    path("<str:pk>/delete/", views.VulnDelete.as_view(), name="vulnerability-delete"),

    path('vulnerabilities/<str:pk>/export-pdf/', views.VulnerabilityExport.as_view(), name="vulnerability-export-pdf"),
    path('vulnerabilities/<str:pk>/export-advisory/', views.VulnerabilityAdvisoryExport.as_view(),
         name="vulnerability-export-advisory"),
    path('vulnerabilities/<str:pk>/notify-vendor/',
         views.VulnerabilityNotifyVendor.as_view(), name="vulnerability-notify-vendor"),
    path('vulnerabilities/<int:pk>/add-log-item/', views.VulnerabilityLogCreate.as_view(),
         name="vulnerability-log-create"),
    path('vulnerabilities/<int:pk>/timeline/', views.VulnerabilityTimeline.as_view(), name="vulnerability-timeline"),
    path('vulnerabilities/<int:pk>/proofs/', views.VulnerabilityProofs.as_view(), name="vulnerability-proofs"),
    path('vulnerabilities/<int:pk>/proofs/text/create/', views.TextProofCreate.as_view(), name="text-proof-create"),
    path('vulnerabilities/<int:pk>/proofs/image/create/', views.ImageProofCreate.as_view(), name="image-proof-create"),

    path('vulnerabilities/<int:pk>/vendor/invite/', views.InviteVendor.as_view(), name="invite-vendor"),

    path('vulnerabilities/<int:pk>/manage-access/', views.ManageAccessList.as_view(), name="manage-access"),
    path('vulnerabilities/<int:pk>/unshare/', views.UnshareVulnerabilityFromUser.as_view(),
         name="unshare-vulnerability"),

    # comments
    path('vulnerabilities/<int:pk>/comments/', views.CommentList.as_view(), name="comment-list"),
    path('vulnerabilities/<int:pk>/comments/create/', views.CommentCreate.as_view(), name="comment-create"),

    # proofs
    path('proofs/text/<str:pk>/delete/', views.TextProofDelete.as_view(), name="text-proof-delete"),
    path('proofs/text/<str:pk>/update/', views.TextProofUpdate.as_view(), name="text-proof-update"),
    path('proofs/image/<str:pk>/delete/', views.ImageProofDelete.as_view(), name="image-proof-delete"),
    path('proofs/image/<str:pk>/update/', views.ImageProofUpdate.as_view(), name="image-proof-update")
]
