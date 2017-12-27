from django import forms

from .models import *


class FormForm(forms.ModelForm):
    """
    Form form
    Author: Nader Alexan
    """

    class Meta:
        model = Form
        fields = ('title', 'external', 'share')


class SubmitFormForm(forms.ModelForm):
    """
    SubmitForm form
    Author: Nader Alexan
    """

    class Meta:
        model = SubmitForm
        fields = ('visitor_email',)


class QuestionForm(forms.ModelForm):
    """
    Question form
    Author: Nader Alexan
    """

    class Meta:
        model = Question
        fields = ('question', 'required', 'type', 'multiple', 'choices')
