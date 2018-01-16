from django import forms

from .models import Applicant


class ApplicantForm(forms.ModelForm):
    class Meta:
        exclude = ['timeline', 'ixp']
        model = Applicant
        fields = '__all__'
