from django.utils import timezone
from vulnman.core.test.testcase_mixin import VulnmanTestCaseMixin
from apps.projects.models import ProjectAPIToken


class VulnmanAPITestCaseMixin(VulnmanTestCaseMixin):
    def create_api_token(self, project, user, date_valid=None):
        if not date_valid:
            date_valid = timezone.now() + timezone.timedelta(days=3)
        token = self._create_instance(ProjectAPIToken, user=user, project=project, date_valid=date_valid)
        return token

    def get_request_kwargs(self, token):
        kwargs = {"HTTP_AUTHORIZATION": "Token %s" % token.key}
        return kwargs
