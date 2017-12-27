from django import forms
from ..models import Profile

choices = (
    (2, 'NATIONAL ID MISMATCH'),
    (3, 'OTHER'),
)


class DeclineForm(forms.ModelForm):
    verification_issue = forms.ChoiceField(label='', initial=2,
                                           widget=forms.RadioSelect(),
                                           choices=choices, required=True,)
    verification_issue_extra = forms.CharField(required=False, label='Notes')

    class Meta:
        model = Profile
        fields = [
            'verification_issue',
            'verification_issue_extra',
        ]
