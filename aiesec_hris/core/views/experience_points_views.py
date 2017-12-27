from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import UpdateView

from .mixins import JsonFormInvalidMixin
from ..models import ExperiencePoints


class ExperiencePointsUpdate(
    LoginRequiredMixin,
    JsonFormInvalidMixin,
    UpdateView):
    model = ExperiencePoints
    template_name = 'experience_points_form.html'
    fields = [
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

    def form_valid(self, form):
        ep = form.save(commit=False)
        ep.user = self.request.user
        ep.save()
        success_message = 'Experience Points updated successfully'
        return JsonResponse({
            'details': success_message,
            'success_url': self.request.user.profile.get_absolute_url()})
