from django.urls import path
from apps.projects import views


app_name = "clients"

urlpatterns = [
    path("", views.ClientList.as_view(), name="client-list"),
    path("create/", views.ClientCreate.as_view(), name="client-create"),
    path("<str:pk>/", views.ClientDetail.as_view(), name="client-detail"),
    path("<str:pk>/update/", views.ClientUpdate.as_view(), name="client-update"),
    path("<str:pk>/delete/", views.ClientDelete.as_view(), name="client-delete"),
    path("<str:pk>/contacts/", views.ClientContacts.as_view(), name="client-contacts"),
    path("<str:pk>/contacts/create/", views.ContactCreate.as_view(), name="contact-create"),

    path("contacts/<str:pk>/delete/", views.ContactDelete.as_view(), name="contact-delete")
]
