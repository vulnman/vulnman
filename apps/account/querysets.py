from django.db.models import QuerySet


class PentestProfileQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(user__is_active=True, user__user_role=user.USER_ROLE_PENTESTER, user=user)
