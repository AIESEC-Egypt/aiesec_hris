from django import forms

from .models import Applicant


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ['timeline', 'ixp']
        fields = '__all__'
