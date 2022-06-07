from vulnman.core.tests.mixins.core import CoreObjectsTestCaseMixin, SessionAuthHelperTestCaseMixin


class VulnmanViewTestCaseMixin(CoreObjectsTestCaseMixin, SessionAuthHelperTestCaseMixin):
    def init_mixin(self):
        super().init_mixin()

    def _test_listview_status_code(self, url, status_code=200):
        pass
