from guardian.shortcuts import assign_perm, remove_perm, get_perms


class ProjectPermissionHandler(object):
    # not yet used
    project_permissions = []

    def __init__(self, project, user):
        self.project = project
        self.user = user

    def get_project_permissions(self):
        return self.project_permissions.copy()

    def assign_project_permissions(self):
        """
        Assign permissions to the project
        """
        self.remove_project_permissions()
        for perm in self.get_project_permissions():
            assign_perm(perm, user_or_group=self.user, obj=self.project)

    def remove_project_permissions(self):
        for perm in get_perms(self.user, self.project):
            remove_perm(perm)


class PentesterRolePermissionHandler(ProjectPermissionHandler):
    project_permissions = [
        "projects.view_project", "projects.change_project",
    ]
