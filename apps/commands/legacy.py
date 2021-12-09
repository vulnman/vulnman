

class QueueCommandForm(forms.Form):
    command = forms.ModelChoiceField(queryset=models.SuggestedCommand.objects.all())
    hosts = forms.ModelMultipleChoiceField(queryset=Host.objects.all())
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all())
    threat_ip_as_domain = forms.BooleanField()
    overwrite_scheme = forms.CharField(max_length=12)

    class Meta:
        fields = '__all__'

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hosts'].queryset = Host.objects.filter(project=project)
        self.fields['services'].queryset = Service.objects.filter(host__project=project)




class SuggestedCommandForm(forms.ModelForm):
    class Meta:
        model = models.SuggestedCommand
        exclude = ["creator", "uuid", "methodology"]

class SuggestedCommandInline(InlineFormSetFactory):
    model = models.SuggestedCommand
    exclude = ["uuid", "creator"]
    factory_kwargs = {'extra': 1, 'can_delete': True, 'max_num': 15}



class SuggestedCommandUpdate(generic.VulnmanAuthUpdateView):
    template_name = "methodologies/suggested_command_update.html"
    form_class = forms.SuggestedCommandForm
    model = models.SuggestedCommand
    extra_context = {'TEMPLATE_HIDE_BREADCRUMBS': True}

    def get_success_url(self):
        return reverse_lazy('methodology:methodology-detail', kwargs={'pk': self.get_object().methodology.pk})


class CommandQueue(generic.ProjectFormView):
    template_name = "methodologies/command_queue.html"
    form_class = forms.QueueCommandForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs


"""
    <div class="list-group mt-3">
        {% for item in methodology.suggestedcommand_set.all %}
            <li class="list-group-item">
                <div class="row">
                    <div class="col-sm-12">
                        <div class="clearfix">
                            <div class="float-start">
                                <h4>{{ item.name }}</h4>
                            </div>
                            <div class="float-end">
                                <a href="{% url 'methodology:suggested-command-update' item.pk %}">
                                    <i class="fa fa-edit"></i> Edit</a>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-sm-12">
                        <pre class="code">
                            {{ item|parse_command:request }}
                        </pre>
                        </div>
                    </div>
            </li>
        {% endfor %}
    </div>
"""