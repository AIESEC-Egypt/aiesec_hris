from django.views.generic import TemplateView

from ..models import LC
from .mixins import MCRequiredMixin


class StatsView(MCRequiredMixin, TemplateView):
    template_name = 'stats.html'
    fields = (
        'title',
        'experience_points_score',
        'num_members',
        'num_tasks',
        'num_tasks_accepted_before_deadline',
        'num_tasks_submitted_after_deadline',
        'num_new_tasks',
        'num_submitted_tasks',
        'num_accepted_tasks',
        'num_rejected_tasks',
        'num_events'
    )

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context.update({
            'lcs': LC.objects.all(),
            'fields': self.fields
        })
        return context
