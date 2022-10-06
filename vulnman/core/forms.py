from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5 import bootstrap5


class DateInput(forms.DateInput):
    input_type = 'date'


class CodeMirrorWidget(forms.Textarea):
    @property
    def media(self):
        js = ['js/jquery.min.js', 'js/codemirror/codemirror.min.js', 'js/codemirror/markdown.min.js']
        css = ['css/codemirror.min.css']
        return forms.Media(
            css={'all': css},
            js=js
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = [
            super().render(name, value, attrs, renderer),
            '<script>var id_%s = CodeMirror.fromTextArea(document.getElementById("id_%s"), '
            '{mode: "markdown", lineWrapping: true});$("#id_%s").attr("required", false);</script>' % (
                name, name, name
            )
        ]
        return mark_safe("\n".join(output))


class FileDropWidget(forms.FileInput):

    @property
    def media(self):
        js = ["vendor/filepond/filepond.min.js", "vendor/filepond/filepond.jquery.js"]
        css = ["vendor/filepond/filepond.css"]
        return forms.Media(
            css={'all': css}, js=js
        )

    def render(self, name, value, attrs=None, renderer=None):
        script = "<script>$('#id_%s').filepond({storeAsFile:true,credits:false});</script>" % name
        output = [
            super().render(name, value, attrs, renderer),
            script
        ]
        return mark_safe("\n".join(output))


class BaseCrispyModelForm(forms.ModelForm):
    def get_layout(self):
        fields = []
        for field in self.fields:
            fields.append(layout.Row(layout.Div(bootstrap5.FloatingField("name"), css_class="col-sm-12",)))
        form_layout = layout.Layout(
            *fields,
            layout.Row(
                FormActions(layout.Submit("submit", "Submit", css_class="btn btn-primary w-100"),
                            wrapper_class="col-sm-12 col-md-6")
            )
        )
        return form_layout

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = self.get_layout()
