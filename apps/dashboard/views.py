from vulnman.core.views import generics
from django.views.generic import RedirectView
from django.urls import reverse_lazy


class Index(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('projects:project-list')
        return reverse_lazy('account:login')


class Dashboard(generics.VulnmanAuthTemplateView):
    template_name = "dashboard/dashboard.html"
