from collections.abc import Mapping
from django.db import transaction
from rest_framework.serializers import Serializer, ModelSerializer, ValidationError
from django.contrib.auth.models import Group, User
from guardian.shortcuts import assign_perm
from apps.projects.models import Project


class ObjectPermissionsAssignmentSerializerMixin(Serializer):
    """
    Original Source: https://github.com/rpkilby/django-rest-framework-guardian/blob/master/src/rest_framework_guardian/serializers.py
    A serializer mixin that provides an easy way to assign permissions
    to given users and/or group when an object is created or updated.
    """
    def save(self, **kwargs):
        created = self.instance is not None
        result = super().save(**kwargs)
        permissions_map = self.get_permissions_map(created)
        self.assign_permissions(permissions_map)
        return result

    def get_permissions_map(self, created):
        """
        Return a map where keys are permissions and values are a list of users and/or groups
        """
        raise NotImplementedError

    def assign_permissions(self, permissions_map):
        """
        Assign the permissions to their associated users/groups
        """
        assert isinstance(permissions_map, Mapping), (
            'Expected %s.get_permissions_map to return a dict, got %s instead.'
            % (self.__class__.__name__, type(permissions_map).__name__)
        )
        with transaction.atomic():
            for permission, assignees in permissions_map.items():
                users = [u for u in assignees if isinstance(u, User)]
                groups = [g for g in assignees if isinstance(g, Group)]
                for user in users:
                    assign_perm(permission, user, self.instance)
                for group in groups:
                    assign_perm(permission, group, self.instance)


class AssignObjectPermissionsModelSerializer(ObjectPermissionsAssignmentSerializerMixin, ModelSerializer):
    pass


class ProjectRelatedObjectSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow project to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            if self.fields.get('project'):
                self.fields.get('project').read_only = True

    def validate_project(self, project):
        if self.context["request"].user.has_perm("projects.change_project", project):
            return project
        raise ValidationError("Could not find project!")


"""
Example Usage:

class PostSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        readers = Group.objects.get(name='readers')
        supervisors = Group.objects.get(name='supervisors')

        return {
            'view_post': [current_user, readers],
            'change_post': [current_user],
            'delete_post': [current_user, supervisors]
        }
"""