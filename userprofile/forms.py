from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import UserProfile
from django.utils.translation import ugettext, ugettext_lazy as _


class UserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('profile_picture', 'hobbies')