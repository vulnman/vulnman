from django.conf import settings


class ThemeMixin(object):
    """
    Mixin that adds a CSS theme to the context
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_theme_file'] = "css/themes/%s.min.css" % settings.VULNMAN_CSS_THEME
        return context
