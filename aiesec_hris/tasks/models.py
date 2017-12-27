from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from aiesec_hris.comments.models import Comment
from aiesec_hris.notifications.models import Notification
from aiesec_hris.users.models import User


class Task(models.Model):
    """
    Model representing a task
    Author: Nader Alexan
    """
    TASK_STATUS_CHOICES = (
        (1, 'NEW'),
        (2, 'SUBMITTED'),
        (3, 'ACCEPTED'),
        (4, 'REJECTED'),)
    TASK_SUBMISSION_TYPE_CHOICES = (
        (1, 'TEXTUAL'),
        (2, 'NUMERIC'),)
    assigner = models.ForeignKey(User, related_name='assigner', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE)
    comments = GenericRelation(Comment)
    notifications = GenericRelation(Notification, related_query_name='task')

    title = models.CharField(max_length=128)
    description = models.TextField()
    status = models.IntegerField(choices=TASK_STATUS_CHOICES, default=1)
    submission_type = models.IntegerField(
        choices=TASK_SUBMISSION_TYPE_CHOICES, default=1)
    submission = models.TextField(null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField()

    def __str__(self):
        return '%s to %s: %s' % (
            self.assigner.get_full_name(),
            self.assignee.get_full_name(),
            self.title)

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        creation = not self.pk

        if creation:
            super(Task, self).save(*args, **kwargs)
            Notification(
                receiver=self.assignee,
                content_object=self,
                action=1,
                text='A task titled "%s" has been assigned to you by %s' % (
                    self.title, self.assigner.get_full_name())
            ).save()
        else:
            pre_save_status = Task.objects.get(pk=self.pk).status
            super(Task, self).save(*args, **kwargs)
            # check status change
            if pre_save_status != self.status:
                # check task submitted
                if self.status == 2:
                    Notification(
                        receiver=self.assigner,
                        content_object=self,
                        action=3,
                        text='The task titled "%s" has been submitted by %s' % (
                            self.title, self.assignee.get_full_name())
                    ).save()
                # check task accepted/rejected
                if self.status in [3, 4]:
                    Notification(
                        receiver=self.assignee,
                        content_object=self,
                        action=2,
                        text='The task titled "%s" has been %s by %s' % (
                            self.title,
                            self.get_status_display().lower(),
                            self.assigner.get_full_name())
                    ).save()

    class Meta:
        ordering = ['-deadline']
