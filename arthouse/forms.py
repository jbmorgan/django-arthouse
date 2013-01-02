from django.forms import Form, ModelForm, ValidationError

from bootstrapforms import BootstrapForm, BootstrapModelForm, BootstrapUserCreationForm, BootstrapPasswordChangeForm

from arthouse import models

class UserCreationForm(BootstrapUserCreationForm):

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        return super(UserCreationForm, self).clean_password2()


class UserUpdateForm(BootstrapPasswordChangeForm):

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        return super(UserUpdateForm, self).clean_new_password2()

class MovieCreateForm(BootstrapModelForm):
    """
    Used by ``MovieCreateView`` to allow users to create a new ``Movie``.
    """

    class Meta:
        model = models.Movie