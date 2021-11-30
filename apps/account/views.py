from django.contrib.auth import views
from django.urls import reverse_lazy
from apps.account import forms
from vulnman.mixins import ThemeMixin
from vulnman.views import generic


class Login(ThemeMixin, views.LoginView):
    template_name = "account/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['TEMPLATE_HIDE_BREADCRUMBS'] = True
        return context


class Logout(views.LogoutView):
    pass


class ProfileEdit(generic.VulnmanAuthUpdateView):
    form_class = forms.ProfileForm
    template_name = "account/profile_edit.html"
    success_url = reverse_lazy('projects:project-list')

    def get_object(self, queryset=None):
        return self.request.user.profile
