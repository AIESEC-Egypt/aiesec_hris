from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'notes',
            'invitees')
