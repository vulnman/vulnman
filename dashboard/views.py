from vulnman.views import generic
from django.views.generic import RedirectView
from django.urls import reverse_lazy


class Index(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('dashboard:dashboard')
        return reverse_lazy('account:login')


class Dashboard(generic.VulnmanAuthTemplateView):
    template_name = "dashboard/dashboard.html"
