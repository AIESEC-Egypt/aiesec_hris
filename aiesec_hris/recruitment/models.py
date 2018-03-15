from datetime import datetime
from django.utils import timezone

from django.db import models

# Create your models here.
from aiesec_hris.users.models import User


class Timeline(models.Model):
    status_applied = models.BooleanField(default=True)
    date_applied = models.DateTimeField(default=timezone.now)

    status_contacted = models.BooleanField(default=False)
    date_contacted = models.DateTimeField(default=None, null=True)
    user_contacted = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                       related_name="user_contacted")

    status_onhold = models.BooleanField(default=False)
    date_onhold = models.DateTimeField(default=None, null=True)
    user_onhold = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                    related_name="user_onhold")

    status_accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(default=None, null=True)
    user_accepted = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                      related_name="user_accepted")

    status_rejected = models.BooleanField(default=False)
    date_rejected = models.DateTimeField(default=None, null=True)
    user_rejected = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                      related_name="user_rejected")

    status_inducted = models.BooleanField(default=False)
    date_inducted = models.DateTimeField(default=None, null=True)
    user_inducted = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING,
                                      related_name="user_inducted")

    current_status = models.CharField(max_length=128, blank=True, null=True)

    def change_status(self):
        if self.status_applied and self.status_contacted and not self.status_rejected and not self.status_accepted and not self.date_onhold:
            self.current_status = 'contacted'
        if self.status_applied and self.status_contacted and self.status_accepted and not self.status_rejected and not self.status_onhold:
            self.current_status = 'accepted'
        if self.status_applied and self.status_contacted and self.status_rejected and not self.status_accepted and not self.status_onhold:
            self.current_status = 'rejected'
        if self.status_applied and self.status_contacted and self.status_onhold and not self.status_accepted and not self.status_rejected:
            self.current_status = 'on_hold'
        if self.status_applied and self.status_contacted and self.status_accepted and self.status_inducted:
            self.current_status = 'inducted'
        self.save()


class Applicant(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    university = models.CharField(max_length=128)
    faculty = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    interested_ixp = models.CharField(max_length=128)
    ixp = models.BooleanField(default=False)
    question_why = models.TextField()
    question_expectations = models.TextField()
    question_time = models.CharField(max_length=128)
    question_uniqueness = models.TextField()

    # Questionnaire

    timeline = models.OneToOneField(Timeline, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def contact(self, User):
        self.timeline.status_contacted = True
        self.timeline.date_contacted = timezone.now()
        self.timeline.user_contacted = User
        self.timeline.save()
        self.timeline.change_status()

    def accept(self):
        self.timeline.status_accepted = True
        self.timeline.date_accepted = datetime.now()
        self.timeline.change_status()

    def reject(self):
        self.timeline.status_rejected = True
        self.timeline.date_rejected = datetime.now()
        self.timeline.change_status()

    def hold(self):
        self.timeline.status_onhold = True
        self.timeline.date_onhold = datetime.now()
        self.timeline.change_status()

    def induct(self):
        self.timeline.status_inducted = True
        self.timeline.date_inducted = datetime.now()
        self.timeline.change_status()
