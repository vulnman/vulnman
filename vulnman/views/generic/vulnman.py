from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from vulnman import mixins


class VulnmanListView(mixins.VulnmanContextMixin, generic.ListView):
    pass


class VulnmanDetailView(mixins.VulnmanContextMixin, generic.DetailView):
    pass


class VulnmanUpdateView(mixins.VulnmanContextMixin, SuccessMessageMixin, generic.UpdateView):
    success_message = "Object updated successfully"


class VulnmanDeleteView(mixins.VulnmanContextMixin, generic.DeleteView):
    pass


class VulnmanCreateView(mixins.VulnmanContextMixin, SuccessMessageMixin, generic.CreateView):
    success_message = "Object created successfully"


class VulnmanAuthListView(LoginRequiredMixin, VulnmanListView):
    pass


class VulnmanAuthDetailView(LoginRequiredMixin, VulnmanDetailView):
    pass


class VulnmanAuthUpdateView(LoginRequiredMixin, VulnmanUpdateView):
    pass


class VulnmanAuthDeleteView(LoginRequiredMixin, VulnmanDeleteView):
    pass


class VulnmanAuthCreateView(LoginRequiredMixin, VulnmanCreateView):
    pass


class VulnmanAuthCreateWithInlinesView(LoginRequiredMixin, mixins.ThemeMixin, SuccessMessageMixin,
                                       CreateWithInlinesView):
    success_message = "Object created successfully"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class VulnmanAuthUpdateWithInlinesView(LoginRequiredMixin, mixins.ThemeMixin, SuccessMessageMixin,
                                       UpdateWithInlinesView):
    success_message = "Object updated successfully"


class VulnmanAuthTemplateView(LoginRequiredMixin, mixins.ThemeMixin, generic.TemplateView):
    pass


class VulnmanAuthFormView(LoginRequiredMixin, mixins.ThemeMixin, generic.FormView):
    pass


class VulnmanAuthRedirectView(LoginRequiredMixin, mixins.ThemeMixin, generic.RedirectView):
    pass
