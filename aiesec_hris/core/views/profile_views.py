from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import JsonFormInvalidMixin
from ..models import Profile, Position


class ProfileQuerysetBase(LoginRequiredMixin, View):
    model = Profile
    fields = [
        'lc',
        'job_description',
        'address',
        'phone',
        'expa_id',
        'national_id_number',
        'gender',
        'date_of_birth',
        'has_ixp'
    ]
    experience_points_fields = [
        'introduction',
        'plan',
        'personal_goal_setting',
        'regular_team_meeting',
        'regular_one_to_ones',
        'team_day',
        'report',
        'transition',
        'debrief',
    ]


class ProfileDetail(ProfileQuerysetBase, DetailView):
    template_name = 'profiles/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        context['experience_points_fields'] = self.experience_points_fields
        return context

    def get_queryset(self):
        position = self.request.user.profile.position
        # MC user, allowed access to all profiles
        if position.type == 1:
            return Profile.objects.all()
        return position.lc.profile.all()


class ProfileUpdate(JsonFormInvalidMixin, ProfileQuerysetBase, UpdateView):
    template_name = 'profiles/profile_form.html'

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        self.object = form.save()
        success_message = 'Profile updated successfully'
        messages.success(self.request, success_message)
        return JsonResponse({'details': success_message})

    def get_queryset(self):
        position = self.request.user.profile.position
        # MC user, allowed access to all profiles
        if position.type == 1:
            return Profile.objects.all()
        # LC user, allowed access to positions lower within the same LC
        positions = Position.objects.filter(
            position.q_children()).values_list('pk', flat=True)
        # add user's position
        positions = list(positions) + [position.pk]
        return Profile.objects.filter(position__in=positions)
