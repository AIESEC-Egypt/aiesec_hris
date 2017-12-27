from django import forms

from aiesec_hris.users.models import User
from ..models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'lc',
            'position',
            'job_description',
            'address',
            'phone',
            'photo',
            'expa_id',
            'national_id_number',
            'national_id_picture',
            'gender',
            'date_of_birth',
            'has_ixp',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exists')
        return email
