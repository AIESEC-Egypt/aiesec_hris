import factory
from django.contrib.auth.models import User

from ..models import ExperiencePoints


class ExperiencePointsFactory(factory.DjangoModelFactory):
    class Meta:
        model = ExperiencePoints

    user = factory.Iterator(User.objects.all())

    introduction = factory.Iterator([True, False])
    plan = factory.Iterator([True, False])
    personal_goal_setting = factory.Iterator([True, False])
    regular_team_meeting = factory.Iterator([True, False])
    regular_one_to_ones = factory.Iterator([True, False])
    team_day = factory.Iterator([True, False])
    report = factory.Iterator([True, False])
    transition = factory.Iterator([True, False])
    debrief = factory.Iterator([True, False])
