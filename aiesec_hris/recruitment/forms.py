from django import forms

from .models import Applicant


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'

    widgets = {
        'id_email': forms.EmailInput(attrs={'class': 'form-control col-md-6 form-group'}),
    }
