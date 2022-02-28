<<<<<<< HEAD:vulnman/api/mixins.py
from guardian.shortcuts import get_objects_for_user
from apps.projects.models import Project


=======
>>>>>>> origin/dev:vulnman/api/mixins/__init__.py
class IgnoreFieldsAfterCreationMixin(object):
    ignore_fields_after_creation = None

    def get_ignore_fields_after_creation(self):
        if not self.ignore_fields_after_creation:
            return []
        return self.ignore_fields_after_creation

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        for field in self.get_ignore_fields_after_creation():
            if request.data.get(field):
                request.data.pop(field)
        request.data._mutable = False
<<<<<<< HEAD:vulnman/api/mixins.py
        return super().update(request, *args, **kwargs)


class ProjectPermissionMixin(object):
    def get_objects_for_user(self, perm, obj, use_groups=False):
        return get_objects_for_user(self.request.user, perm, obj, use_groups=use_groups)

    def get_project(self, project_pk):
        if not project_pk:
            return None
        projects = get_objects_for_user(self.request.user, "pentest_project", Project.objects.filter(pk=project_pk),
                                        use_groups=False)
        if projects.exists():
            return projects.get()
        return None

    def test_func(self):
        project = self.get_project(serializer.validated_data["project"])
        if project:
            return True
        return PermissionError

    def perform_update(self, serializer):
        self.test_func(serializer)
        super().perform_update(serializer)
=======
        return super().update(request, *args, **kwargs)
>>>>>>> origin/dev:vulnman/api/mixins/__init__.py
