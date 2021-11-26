from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from vulnman import mixins


class VulnmanListView(mixins.ThemeMixin, generic.ListView):
    pass


class VulnmanDetailView(mixins.ThemeMixin, generic.DetailView):
    pass


class VulnmanUpdateView(mixins.ThemeMixin, generic.UpdateView):
    pass


class VulnmanDeleteView(mixins.ThemeMixin, generic.DeleteView):
    pass


class VulnmanCreateView(mixins.ThemeMixin, generic.CreateView):
    pass


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


class VulnmanAuthCreateWithInlinesView(LoginRequiredMixin, mixins.ThemeMixin, CreateWithInlinesView):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class VulnmanAuthUpdateWithInlinesView(LoginRequiredMixin, mixins.ThemeMixin, UpdateWithInlinesView):
    pass


class VulnmanAuthTemplateView(LoginRequiredMixin, mixins.ThemeMixin, generic.TemplateView):
    pass


class VulnmanAuthFormView(LoginRequiredMixin, mixins.ThemeMixin, generic.FormView):
    pass
