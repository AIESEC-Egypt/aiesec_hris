from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from aiesec_hris.users.models import User


class Notification(models.Model):
    """
    Model representing a notification
    Author: Nader Alexan
    """
    NOTIFICATION_ACTION_CHOICES = (
        (1, 'TASK CREATED'),
        (2, 'TASK ACCEPTED/REJECTED'),
        (3, 'TASK SUBMITTED'),
        (10, 'EVENT INVITE'),
        (20, 'FORM INVITE')
    )
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    custom_link = models.TextField(
        null=True,
        blank=True,
        help_text='Link to redirect to, if left empty, the absolute url of the content object is used')
    text = models.TextField()
    action = models.IntegerField(choices=NOTIFICATION_ACTION_CHOICES)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']
