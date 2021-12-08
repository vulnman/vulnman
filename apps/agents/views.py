from django.urls import reverse_lazy
from vulnman.views import generic
from apps.agents import forms
from apps.agents import models


class AgentCreate(generic.VulnmanAuthCreateView):
    template_name = "agents/agent_create.html"
    form_class = forms.AgentForm
    success_url = reverse_lazy('agents:agent-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AgentList(generic.VulnmanAuthListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        return models.Agent.objects.filter(user=self.request.user)


class AgentDelete(generic.VulnmanAuthDeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy('agents:agent-list')

    def get_queryset(self):
        return models.Agent.objects.filter(user=self.request.user)
