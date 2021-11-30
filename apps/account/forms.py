from django import forms
from apps.account import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ["user"]
