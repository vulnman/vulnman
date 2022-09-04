from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.urls import reverse_lazy
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from two_factor.utils import default_device
from apps.projects.models import Project
from apps.account import signals


class UserAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    # if you change this, change migration 0014_user_user_role.py, which did not recognize
    # these attributes in the first run
    USER_ROLE_PENTESTER = 0
    USER_ROLE_VENDOR = 1
    USER_ROLE_CUSTOMER = 2

    USER_ROLE_CHOICES = [
        (USER_ROLE_PENTESTER, "Pentester"),
        (USER_ROLE_CUSTOMER, "Customer"),
        (USER_ROLE_VENDOR, "Vendor")
    ]

    email = models.EmailField(unique=True)
    objects = UserAccountManager()
    user_role = models.PositiveIntegerField(choices=USER_ROLE_CHOICES, null=True)

    class Meta:
        db_table = 'auth_user'
        permissions = [
            ("invite_vendor", "Invite Vendor")
        ]

    @property
    def profile(self):
        if self.user_role == User.USER_ROLE_PENTESTER:
            return self.pentester_profile
        elif self.user_role == User.USER_ROLE_VENDOR:
            return self.vendor_profile

    def has_2fa_enabled(self):
        if default_device(self):
            return True
        return False


class PentesterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="pentester_profile")
    is_public = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)
    public_real_name = models.BooleanField(default=False, help_text="Show your real name on public profile page")
    public_email_address = models.BooleanField(default=False, help_text="Show email address on public profile page")

    hide_name_in_report = models.BooleanField(
        default=False, help_text="Use username in report instead of real name")

    def get_completed_projects(self):
        return self.user.project_set.filter(status=Project.PENTEST_STATUS_CLOSED).count()

    def get_absolute_url(self):
        return reverse_lazy("account:user-profile", kwargs={"slug": self.user.username})


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_role == User.USER_ROLE_PENTESTER:
        PentesterProfile.objects.create(user=instance)
        group = Group.objects.get(name="Pentesters")
        instance.groups.add(group)
        instance.save()
    if created and instance.user_role == User.USER_ROLE_VENDOR:
        VendorProfile.objects.create(user=instance)
        group = Group.objects.get(name="Vendors")
        instance.groups.add(group)
        instance.save()
    if created and instance.user_role == User.USER_ROLE_CUSTOMER:
        group = Group.objects.get(name="Customers")
        instance.groups.add(group)
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.save()


post_migrate.connect(signals.populate_groups_and_permission, sender=None)
