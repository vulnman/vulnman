from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.urls import reverse_lazy
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from apps.projects.models import Project
from apps.account import signals


class UserAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserAccountManager()
    is_pentester = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user'
        permissions = [
            ("invite_vendor", "Invite Vendor")
        ]

    @property
    def profile(self):
        if self.is_pentester:
            return self.pentester_profile
        elif self.is_vendor:
            return self.vendor_profile


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
    if created and instance.is_pentester:
        PentesterProfile.objects.create(user=instance)
        group = Group.objects.get(name="Pentesters")
        instance.groups.add(group)
        instance.save()
    if created and instance.is_vendor:
        VendorProfile.objects.create(user=instance)
        group = Group.objects.get(name="Vendors")
        instance.groups.add(group)
        instance.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_pentester:
        instance.pentester_profile.save()
    elif instance.is_vendor:
        instance.vendor_profile.save()


post_migrate.connect(signals.populate_groups_and_permission, sender=None)
