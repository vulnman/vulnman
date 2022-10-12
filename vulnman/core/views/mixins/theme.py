from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from two_factor.utils import default_device


class ThemeMixin(object):
    """
    Mixin that adds a CSS theme to the context
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_css_file'] = settings.CUSTOM_CSS_FILE
        return context


class TOTPRequiredMixin:
    # TODO: write test
    """
    View mixin which verifies that the user logged in using OTP.
    .. note::
       This mixin should be the left-most base class.
    """
    raise_anonymous = False
    """
    Whether to raise PermissionDenied if the user isn't logged in.
    """

    login_url = settings.LOGIN_URL
    """
    If :attr:`raise_anonymous` is set to `False`, this defines where the user
    will be redirected to. Defaults to ``two_factor:login``.
    """

    redirect_field_name = REDIRECT_FIELD_NAME
    """
    URL query name to use for providing the destination URL.
    """

    raise_unverified = False
    """
    Whether to raise PermissionDenied if the user isn't verified.
    """

    verification_url = reverse_lazy("account:setup-2fa")
    """
    If :attr:`raise_unverified` is set to `False`, this defines where the user
    will be redirected to. If set to ``None``, an explanation will be shown to
    the user on why access was denied.
    """

    def get_login_url(self):
        """
        Returns login url to redirect to.
        """
        return self.login_url and str(self.login_url) or reverse_lazy('two_factor:login')

    def get_verification_url(self):
        """
        Returns verification url to redirect to.
        """
        return self.verification_url and str(self.verification_url)

    def dispatch(self, request, *args, **kwargs):
        if not settings.TOTP_ENFORCE_2FA:
            return super().dispatch(request, *args, **kwargs)
        if not request.user or not request.user.is_authenticated or (not request.user.is_verified() and default_device(request.user)):
            # If the user has not authenticated raise or redirect to the login
            # page. Also if the user just enabled two-factor authentication and
            # has not yet logged in since should also have the same result. If
            # the user receives a 'you need to enable TFA' by now, he gets
            # confuses as TFA has just been enabled. So we either raise or
            # redirect to the login page.
            if self.raise_anonymous:
                raise PermissionDenied()
            else:
                return redirect_to_login(request.get_full_path(), self.get_login_url())
        if not request.user.is_verified():
            if self.raise_unverified:
                raise PermissionDenied()
            return redirect_to_login(request.get_full_path(), self.get_verification_url())
        return super().dispatch(request, *args, **kwargs)


class VulnmanContextMixin(TOTPRequiredMixin, ThemeMixin):
    pass
