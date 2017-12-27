# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from aiesec_hris.notifications.models import Notification
from aiesec_hris.users.models import User


class Form(models.Model):
    """
    Author: AmrAnwar
    """
    owner = models.ForeignKey(User, related_name="form_owner", on_delete=models.CASCADE)
    share = models.ManyToManyField(
        User,
        related_name='form_share',
        help_text='Share this with specific people? Leave empty to share with all members',
        blank=True)

    title = models.CharField(max_length=225, blank=False, null=False)
    external = models.BooleanField(
        default=False,
        help_text='Share this form with unregistered users (users who do not have accounts on this system, for example: a recruitment form)? ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forms-detail", kwargs={'pk': self.id})

    def get_submission_url(self):
        return reverse("submission-login", kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        creation = not self.pk
        super(Form, self).save(*args, **kwargs)
        if creation:
            if self.share.exists():
                receivers = self.share.all()
            else:
                receivers = User.objects.all()

            for receiver in receivers:
                Notification(
                    receiver=receiver,
                    content_object=self,
                    action=20,
                    text='A form titled "%s" has been created and you are invited to submit it' % (
                        self.title),
                    custom_link=self.get_submission_url()
                ).save()


class Question(models.Model):
    """
    Question object in Form
    Author: AmrAnwar
    """
    TYPE = (
        (1, 'Multiple Choice'),
        (2, 'Text'),
    )
    form = models.ForeignKey(Form, related_name="question_form", on_delete=models.CASCADE)

    question = models.CharField(max_length=225)
    required = models.BooleanField(default=False, verbose_name='Required?')
    multiple = models.BooleanField(
        default=False,
        help_text='Can the use select more than choice for the answer?',
        verbose_name='Multiple Answers?')
    choices = models.TextField(help_text='Choices, seprated by new lines', null=True, blank=True)
    type = models.IntegerField(choices=TYPE, null=False, default=1)
    order = models.IntegerField(default=1)

    def __str__(self):
        return "%s: %s" % (self.form, self.question)

    def get_choices(self):
        return self.choices.replace('\r', '').split("\n")

    class Meta:
        ordering = ['order']


class Answer(models.Model):
    """
    Answer object for each Question
    Author: AmrAnwar
    """
    question = models.ForeignKey(Question, related_name="answer_question", on_delete=models.CASCADE)

    value = models.CharField(max_length=225, blank=False, null=False)

    def __str__(self):
        return "%s: %s" % (self.question, self.value)


class SubmitForm(models.Model):
    """
    create SubmitForm object after a user submit a form
    Author: AmrAnwar
    """
    form = models.ForeignKey(Form, related_name="submissions", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer, related_name="answers_submit")
    visitor = models.BooleanField(default=False)
    visitor_email = models.CharField(max_length=225, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return "user:%s %s" % (self.user, self.form)
        else:
            return "visitor %s" % self.form

    def get_absolute_url(self):
        return reverse('submission-detail', kwargs={'pk': self.pk})
