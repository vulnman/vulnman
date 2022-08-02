from django.utils import timezone
from vulnman.core.test.testcase_mixin import VulnmanTestCaseMixin
from apps.projects.models import ProjectAPIToken


class VulnmanAPITestCaseMixin(VulnmanTestCaseMixin):
    def init_mixin(self):
        super().init_mixin()
        self.token1 = self.create_api_token(self.project1, self.pentester1)
        self.token2 = self.create_api_token(self.project2, self.pentester2)

    def create_api_token(self, project, user, date_valid=None):
        if not date_valid:
            date_valid = timezone.now() + timezone.timedelta(days=3)
        token = self._create_instance(ProjectAPIToken, user=user, project=project, date_valid=date_valid)
        return token

    def get_request_kwargs(self, token):
        kwargs = {"HTTP_AUTHORIZATION": "Token %s" % token.key}
        return kwargs

    def post(self, url, data, token):
        return self.client.post(url, data, HTTP_AUTHORIZATION="Token %s" % token.key)

    def get(self, url, token):
        return self.client.get(url,  HTTP_AUTHORIZATION="Token %s" % token.key)

    def delete(self, url, token):
        return self.client.delete(url,  HTTP_AUTHORIZATION="Token %s" % token.key)

    def patch(self, url, data, token):
        return self.client.patch(url, data, HTTP_AUTHORIZATION="Token %s" % token.key)