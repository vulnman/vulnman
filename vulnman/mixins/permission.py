from collections.abc import Iterable
from django.contrib.auth.mixins import UserPassesTestMixin
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin as DJPermissionRequiredMixin


class NonObjectPermissionRequiredMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        if not self.permission_required:
            return True
        if isinstance(self.permission_required, str):
            perms = [self.permission_required]
        elif isinstance(self.permission_required, Iterable):
            perms = [p for p in self.permission_required]
        else:
            # return false to prevent accidental leaks
            return False
        has_permissions = all(self.request.user.has_perm(perm) for perm in perms)
        return has_permissions


class ObjectPermissionRequiredMixin(PermissionRequiredMixin):
    raise_exception = True
    return_403 = True


class VulnmanPermissionRequiredMixin(DJPermissionRequiredMixin):
    raise_exception = True
    return_403 = True
