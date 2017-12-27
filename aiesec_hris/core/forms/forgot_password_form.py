from django import forms
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('This email does not exist')
        return email
