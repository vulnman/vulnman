from django.db.models import QuerySet


class HostQuerySet(QuerySet):
    def for_report(self):
        return self.exclude(hide_from_report=True)
