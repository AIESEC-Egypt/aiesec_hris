from django.db import models
from django.db.models.signals import m2m_changed
from django.urls import reverse

from aiesec_hris.notifications.models import Notification
from aiesec_hris.users.models import User


class Event(models.Model):
    """
    Model representing an event

    Notifications are sent to invitees in the signal `invitees_changed`

    Author: Nader Alexan
    """
    owner = models.ForeignKey(User, related_name='events_created', on_delete=models.CASCADE)
    invitees = models.ManyToManyField(
        User, related_name='events_invited', blank=True)

    title = models.CharField(max_length=128)
    notes = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    start_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField()
    end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


def invitees_changed(sender, **kwargs):
    """
    Signal for post_add of invitees to an event
    to send notifications
    Author: Nader Alexan
    """
    action = kwargs.get('action')
    if action == 'post_add':
        pk_set = kwargs.get('pk_set')
        instance = kwargs.get('instance')
        for pk in pk_set:
            Notification(
                receiver=User.objects.get(pk=pk),
                action=10,
                content_object=instance,
                text='You\'ve been invited to the event %s' % instance.title
            ).save()


m2m_changed.connect(invitees_changed, sender=Event.invitees.through)
