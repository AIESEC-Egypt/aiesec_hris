import operator
import os
import random
import string
from functools import reduce

from django.db import models
from django.db.models import F
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse

from aiesec_hris.core.utility import profile_photo_path, national_id_path
from aiesec_hris.events.models import Event
from aiesec_hris.tasks.models import Task
from aiesec_hris.users.models import User


class ExperiencePoints(models.Model):
    user = models.OneToOneField(User, related_name='experience_points', on_delete=models.CASCADE)

    introduction = models.BooleanField(
        default=False,
        help_text='Buidling: Get to know, Team Bonding \
        Induction to the function/area')
    plan = models.BooleanField(
        default=False,
        help_text='Building: Co-creation of Team Purpose, Expectations, \
        Goals, Strategies, Budget, JD, Deadlines')
    personal_goal_setting = models.BooleanField(
        default=False,
        help_text='Building: Set the Individual Goals an dAction Plan, \
        Make Personal Goals for Development')
    regular_team_meeting = models.BooleanField(
        default=False,
        help_text='Performing: Regular Tracking of the Plan \
        and Team Performance, Team Review')
    regular_one_to_ones = models.BooleanField(
        default=False,
        help_text='Performing: Tracking and Coaching of Individual \
        Performance and Personal Goals, Feedback')
    team_day = models.BooleanField(
        default=False,
        help_text='Performing: \
        Team bonding, Team activities, Appreciations')
    report = models.BooleanField(
        default=False,
        help_text='Closing: \
        Key Results Achieved/Not Achieved')
    transition = models.BooleanField(
        default=False,
        help_text='Closing: Knowledge, \
        Skill, Attitude and Document Transfer')
    debrief = models.BooleanField(
        default=False,
        help_text='Closing: Team Experience \
        Debrief, Key Learnings, Next Steps')

    @property
    def score(self):
        return ((
                    self.introduction * 1 +
                    self.plan * 1 +
                    self.personal_goal_setting * 1 +
                    self.regular_team_meeting * 1 +
                    self.regular_one_to_ones * 1 +
                    self.team_day * 1 +
                    self.report * 1 +
                    self.transition * 1 +
                    self.debrief * 1), 9)

    @property
    def children_score(self):
        score = 0
        num_children = 0
        children_positions = self.user.profile.position.children.all()
        for child_position in children_positions:
            for profile in child_position.profile.all():
                ep = profile.user.experience_points
                ep_score, _ = ep.score
                ep_children_score, _ = ep.children_score
                score += ep_score + ep_children_score
                num_children += 1
        return (score, num_children * 9)

    def __str__(self):
        return '%s %s' % (self.user.get_full_name(), self.score)

    class Meta:
        verbose_name = 'Experience Points'
        verbose_name_plural = 'Experience Points'


class LC(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'LC'
        verbose_name_plural = 'LCs'

    def get_absolute_url(self):
        return reverse('lc-detail', kwargs={'pk': self.pk})

    @property
    def experience_points_score(self):
        total_score = 0
        profiles = self.profile.all()
        for profile in profiles:
            score, _ = profile.user.experience_points.score
            total_score += score
        return (total_score, profiles.count() * 9)

    @property
    def num_members(self):
        return self.profile.count()

    @property
    def num_tasks(self):
        return Task.objects.filter(assignee__profile__lc=self).count()

    @property
    def num_new_tasks(self):
        return Task.objects.filter(
            assignee__profile__lc=self, status=1).count()

    @property
    def num_submitted_tasks(self):
        return Task.objects.filter(
            assignee__profile__lc=self, status=2).count()

    @property
    def num_accepted_tasks(self):
        return Task.objects.filter(
            assignee__profile__lc=self, status=3).count()

    @property
    def num_rejected_tasks(self):
        return Task.objects.filter(
            assignee__profile__lc=self, status=4).count()

    @property
    def num_tasks_accepted_before_deadline(self):
        return Task.objects.filter(
            assignee__profile__lc=self,
            status=3,
            submission_date__lte=F('deadline')).count()

    @property
    def num_tasks_submitted_after_deadline(self):
        return Task.objects.filter(
            assignee__profile__lc=self,
            submission_date__gte=F('deadline')).count()

    @property
    def num_events(self):
        return Event.objects.filter(owner__profile__lc=self).count()


class Position(models.Model):
    POSITION_TYPE_CHOICES = (
        (1, 'MC'),
        (2, 'LC'))
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    lc = models.ForeignKey(LC, null=True, blank=True, related_name='position', on_delete=models.CASCADE)

    type = models.IntegerField(choices=POSITION_TYPE_CHOICES)
    title = models.CharField(max_length=128)

    def q_children(self):
        """
        Generates Q queries ORed for all lower positions recursively
        """
        if self.children.exists():
            result = Q(parent=self)
            for child in self.children.all():
                result |= child.q_children()
            return result
        # excludes all results
        return Q(id=-1)

    def __str__(self):
        if self.parent:
            return '%s > %s %s' % (
                self.parent.__str__(), self.type, self.title)
        return '%s %s' % (self.type, self.title)

    def is_parent_of(self, position):
        """
        Check if `self` is a parent of `position`
        """
        current = position
        while current.parent:
            if self == current.parent:
                return True
            current = current.parent
        return False


class ProfileManger(models.Manager):
    def search(self, **kwargs):
        """
        //I used reduce(operator.or_,) to make the search more useful
        >>cause if a staff search using the full name with the old code will get None
        :param kwargs: search << the GET request for search
        :return: the search result << Queryset of profiles
        """
        search = kwargs['search'].strip().split(" ")
        query_first_name = reduce(operator.or_, (Q(user__first_name__contains=item)
                                                 for item in search))
        query_last_name = reduce(operator.or_, (Q(user__last_name__contains=item)
                                                for item in search))
        return super(ProfileManger, self).filter(
            Q(query_first_name) |
            Q(query_last_name) |
            Q(phone__icontains=search)
        ).distinct()


class Profile(models.Model):
    """
    A user's profile.
    Author: Ahmed H. Ismail and Nader Alexan
    """
    VERIFICATION_ISSUES_CHOICES = (
        (1, 'PENDING'),
        (2, 'NATIONAL ID MISMATCH'),
        (3, 'OTHER'),
        (4, 'NONE'))
    GENDER_CHOICES = (
        (1, 'MALE'),
        (2, 'FEMALE'))
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    lc = models.ForeignKey(LC, null=True, blank=True, related_name='profile', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, related_name='profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    manually_verified = models.BooleanField(default=False)
    job_description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to=profile_photo_path)
    expa_id = models.TextField()
    national_id_number = models.CharField(max_length=128)
    national_id_picture = models.ImageField(upload_to=national_id_path)
    verification_issue = models.IntegerField(
        choices=VERIFICATION_ISSUES_CHOICES,
        default=1)
    verification_issue_extra = models.TextField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    has_ixp = models.BooleanField(default=False)

    objects = ProfileManger()

    class Meta:
        ordering = ["-created_at"]

    def delete_photo(self):
        if self.photo and os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
            self.photo = None

    def delete_national_id(self):
        if self.national_id_picture and os.path.isfile(
            self.national_id_picture.path):
            os.remove(self.national_id_picture.path)
            self.national_id_picture = None

    def get_accept_url(self):
        return reverse('moderation-accept', kwargs={'id': self.id})

    def get_decline_url(self):
        return reverse('moderation-decline', kwargs={'id': self.id})

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk': self.pk})

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return '%s' % self.user

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def id_picture(self):
        return self.national_id_picture.url

    def save(self, *args, **kwargs):
        """
        Create experience points instance on creating a profile
        """
        if not self.id:
            ExperiencePoints(user=self.user).save()
        return super(Profile, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Profile)
def delete_file_if_exists(sender, instance, *args, **kwargs):
    instance.delete_photo()
    instance.delete_national_id()


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.code = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(32))
        return super(ResetPasswordCode, self).save(*args, **kwargs)


from django.utils.text import slugify


def create_slug(instance, new_slug=None):
    """
    * Take any instance to make unique slug of his title
        even if 2 instance with the same title
    Author : AmrAnwar
    :param instance:
    :param new_slug: re-send to the function again to make recursive call
    :return: new slug until get unique slug
    """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = instance.__class__.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
