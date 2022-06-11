from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from apps.projects.models import Project, Client, ProjectContributor
from ddf import G
from guardian.shortcuts import assign_perm


class VulnmanTestMixin(object):
    def init_mixin(self):
        self.user1 = self._create_user("dummyuser1", "changeme")
        self.user2 = self._create_user("dummyuser2", "changeme")
        self.pentester1 = self._create_user("pentester", "changeme")
        self.pentester2 = self._create_user("pentester2", "changeme")
        self.read_only1 = self._create_user("readonly1", "changeme")
        self.manager = self._create_user("manager", "changeme")
        self.manager.groups.add(Group.objects.get(name="Management"))
        self.pentester1.groups.add(Group.objects.get(name="Pentesters"))
        self.pentester2.groups.add(Group.objects.get(name="Pentesters"))
        self.project1 = self._create_project(creator=self.pentester1)
        self.project2 = self._create_project(creator=self.pentester2)
        self.add_contributor(self.read_only1, self.project1, role=ProjectContributor.ROLE_READ_ONLY)

    def add_contributor(self, user, project, role=ProjectContributor.ROLE_PENTESTER):
        return ProjectContributor.objects.create(user=user, project=project, role=role)

    def _create_user(self, username, password, is_staff=False):
        email = "%s@example.com" % username
        return User.objects.create_user(username, password=password, is_staff=is_staff, email=email)

    def assign_perm(self, perm, user_or_group, obj=None):
        assign_perm(perm, user_or_group=user_or_group, obj=obj)

    def _create_project(self, client=None, creator=None):
        if not client:
            client = self._create_instance(Client)
        return Project.objects.create(creator=creator, client=client, start_date=timezone.now(),
                                      end_date=timezone.now())

    def get_url(self, endpoint, **kwargs):
        return reverse_lazy(endpoint, kwargs=kwargs)

    def _create_instance(self, obj_class, **kwargs):
        return G(obj_class, **kwargs)

    def _set_session_variable(self, key, value):
        session = self.client.session
        session[key] = value
        session.save()

    def login_with_project(self, user, project):
        self.client.force_login(user)
        self._set_session_variable("project_pk", str(project.pk))

    def _test_unauthenticated_aceess(self, url, expected_status_code=403):
        response = self.client.get(url, follow=True)
        login_url = self.get_url(settings.LOGIN_URL)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(str(login_url) in str(response.redirect_chain[0][0]), True)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, expected_status_code)

    def _test_foreign_access(self, url, foreign_user, project):
        self.login_with_project(foreign_user, project)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class VulnmanAPITestMixin(VulnmanTestMixin):
    def _check_creator_read_only(self, url, obj_class):
        # TODO: use this one
        # TODO: check same for projects
        new_user = self._create_user("temporaryuser", "changeme")
        payload = {"creator": new_user.username}
        self.client.force_login(new_user)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(obj_class.objects.filter(creator=new_user).count(), 0)

    def _test_project_updateview(self, lazy_url, payload, obj_class, project_creator_field="project__creator"):
        project_field = project_creator_field.split("__")[-2]
        project_data = {project_field: self._create_project()}
        # test unauthenticated denied
        temporary_object = self._create_instance(obj_class, **project_data)
        url = self.get_url(lazy_url, pk=temporary_object.pk)
        self.client.logout()
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 403)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, 403)

        # test as temporary user
        new_user = self._create_user("temporaryuserupdateview", "changeme")
        self.client.force_login(new_user)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 404)
        filter_data = {project_creator_field: new_user}
        self.assertEqual(obj_class.objects.filter(**filter_data).count(), 0)

        # test as creator user
        my_object = self._create_instance(obj_class, **filter_data)
        self.client.force_login(new_user)
        url = self.get_url(lazy_url, pk=my_object.pk)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(obj_class.objects.filter(**payload).count(), 1)

    def _test_project_listview(self, lazy_url, obj_class, project_creator_field="project__creator"):
        # test unauthenticated denied
        url = self.get_url(lazy_url)
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # test my object
        my_object_data = {project_creator_field: self.user1}
        my_object = self._create_instance(obj_class, **my_object_data)
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["uuid"], str(my_object.pk))
        # test other object
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def _test_project_createview(self, lazy_url, payload, obj_class, project_creator_field="project__creator",
                                 format='json'):
        url = self.get_url(lazy_url)
        self.client.logout()
        response = self.client.post(url, payload, format=format)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(obj_class.objects.count(), 0)
        project1 = self._create_project(creator=self.user1)
        project2 = self._create_project(creator=self.user2)
        # test my object
        project_field = project_creator_field.split("__")[-2]
        payload[project_field] = str(project1.pk)
        filter_data = {project_field: str(project1.pk)}
        self.client.force_login(self.user1)
        response = self.client.post(url, payload, format=format)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(obj_class.objects.filter(**filter_data).count(), 1)
        # test to create object to foreign project
        payload[project_field] = str(project2.pk)
        response = self.client.post(url, payload, format=format)
        self.assertEqual(response.status_code, 403)

    def _test_project_deleteview(self, lazy_url, obj_class, project_creator_field="project__creator"):
        data = {project_creator_field: self.user1}
        my_object = self._create_instance(obj_class, **data)
        url = self.get_url(lazy_url, pk=my_object.pk)
        self.client.logout()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        # test delete foreign objects
        self.client.force_login(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        # test my object delete
        self.client.force_login(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
