from django.db import models


# Create your models here.


class Timeline(models.Model):
    status_contacted = models.BooleanField(default=False)
    date_contacted = models.DateTimeField(default=False)

    status_onhold = models.BooleanField(default=False)
    date_onhold = models.DateTimeField(default=False)

    status_accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(default=False)

    status_rejected = models.BooleanField(default=False)
    date_rejected = models.DateTimeField(default=False)

    status_inducted = models.BooleanField(default=False)
    date_inducted = models.BooleanField(default=False)


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

    # Questionnaire

    # timeline = models.OneToOneField(Timeline, on_delete=models.CASCADE)


