from django import forms


class ChangePasswordForm(forms.Form):
    """
    Change password form
    Author: Nader Alexan
    """
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.request = request
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password_2(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_2 = self.cleaned_data.get('new_password_2')
        if new_password != new_password_2:
            raise forms.ValidationError(
                'New passwords do not match')
        return new_password

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.request.user.check_password(current_password):
            raise forms.ValidationError('Invalid current password')
        return current_password
