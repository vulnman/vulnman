from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin as DJPermissionRequiredMixin


class ObjectPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Check if a user has object level permissions.
    Raise 403 if not.
    """
    raise_exception = True
    return_403 = True


class VulnmanPermissionRequiredMixin(DJPermissionRequiredMixin):
    """
    Check if user has permissions to perform an action.
    Raise 403 if not.
    """
    raise_exception = True
    return_403 = True
