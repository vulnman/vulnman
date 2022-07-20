from django.db.models import QuerySet


class ReportQuerySet(QuerySet):
    def for_project(self, project):
        self.filter(project=project)
