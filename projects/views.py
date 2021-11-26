from django.http import Http404
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.conf import settings
from django_tex.response import PDFResponse
from django_tex.shortcuts import compile_template_to_pdf
from django_tex.core import render_template_with_context, run_tex
from projects import models
from projects import forms
from vulnman.views import generic


class ProjectList(generic.VulnmanAuthListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        if self.request.session.get('project_pk'):
            del self.request.session['project_pk']
        context = self.get_context_data()
        return self.render_to_response(context)


class ProjectCreate(generic.VulnmanAuthCreateWithInlinesView):
    template_name = "projects/project_create.html"
    form_class = forms.ProjectForm
    model = models.Project
    inlines = [forms.ProjectClassificationInline, forms.ScopeInline, forms.ProjectContactInline]
    success_url = reverse_lazy("projects:project-list")


class ProjectDetail(generic.VulnmanAuthDetailView):
    template_name = "projects/project_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            self.request.session['project_pk'] = str(self.get_object().pk)
        return self.render_to_response(context)

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)


class ProjectUpdate(generic.VulnmanAuthUpdateWithInlinesView):
    template_name = "projects/project_update.html"
    form_class = forms.ProjectForm
    inlines = [forms.ProjectClassificationInline, forms.ScopeInline, forms.ProjectContactInline]
    model = models.Project

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return models.Project.objects.filter(creator=self.request.user)


class ReportList(generic.ProjectListView):
    template_name = "projects/report_list.html"
    paginate_by = 20
    context_object_name = "reports"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project()).order_by('-revision')


class ReportDetail(generic.ProjectDetailView):
    template_name = "report/document.tex"
    context_object_name = "report"

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def render_to_response(self, context, **response_kwargs):
        return PDFResponse(context['report'].pdf_source, filename="report.pdf")


class ReportCreate(generic.ProjectCreateView):
    report_template_name = "report/document.tex"
    template_name = "projects/report_create.html"
    form_class = forms.ReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SEVERITY_COLORS'] = settings.SEVERITY_COLORS
        return context

    def get_success_url(self):
        return reverse_lazy('projects:report-list')

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.creator = self.request.user
        form.save()
        context = self.get_context_data()
        context['report'] = form.instance
        pdf_source = compile_template_to_pdf(self.report_template_name, context)
        latex_source = render_template_with_context(self.report_template_name, context)
        form.instance.latex_source = latex_source
        form.instance.pdf_source = pdf_source
        return super().form_valid(form)


class ReportUpdate(generic.ProjectUpdateView):
    template_name = "projects/report_update.html"
    report_template_name = "report/document.tex"
    form_class = forms.ReportUpdateForm

    def get_queryset(self):
        return models.Report.objects.filter(project=self.get_project())

    def form_valid(self, form):
        try:
            pdf_source = run_tex(form.instance.latex_source)
            form.instance.pdf_source = pdf_source
            return super().form_valid(form)
        except Exception as e:
            form.instance.delete()
            form.delete()
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('projects:report-list', kwargs={'project_pk': self.kwargs.get('project_pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SEVERITY_COLORS'] = settings.SEVERITY_COLORS
        return context
