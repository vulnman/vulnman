from django.conf import settings


class ThemeMixin(object):
    """
    Mixin that adds a CSS theme to the context
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_css_file'] = settings.CUSTOM_CSS_FILE
        return context


class VulnmanContextMixin(ThemeMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RESPONSIBLE_DISCLOSURE_APP_ENABLE'] = settings.RESPONSIBLE_DISCLOSURE_APP_ENABLE
        return context
