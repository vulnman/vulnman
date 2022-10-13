from django import forms
from django.utils.safestring import mark_safe


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
