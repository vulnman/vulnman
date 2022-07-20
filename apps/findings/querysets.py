from django.db.models import QuerySet


class VulnerabilityQuerySet(QuerySet):
    def open(self):
        return self.filter(status=self.model.STATUS_OPEN)

    def fixed(self):
        return self.filter(status=self.model.STATUS_FIXED)

    def for_project(self, project):
        return self.filter(project=project)
