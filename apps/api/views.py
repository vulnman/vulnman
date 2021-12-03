from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class SwaggerUI(LoginRequiredMixin, generic.TemplateView):
    template_name = "api/swagger-ui.html"
