from django.test import TestCase

from ...models import ExperiencePoints
from ...factories import (
    ExperiencePointsFactory,
    UserFactory,
    PositionFactory,
    ProfileFactory,
    LCFactory)


class ExperiencePointsTest(TestCase):

    def test_string_representation(self):
        UserFactory()
        ep = ExperiencePointsFactory()
        self.assertEqual(
            ep.__str__(),
            '%s %s' % (ep.user.get_full_name(), ep.score))

    def test_score(self):
        ep = ExperiencePoints(introduction=True, user=UserFactory())
        ep.save()
        self.assertEqual(ep.score, (1, 9))

    def test_children_score(self):
        LCFactory()
        user = UserFactory()
        position = PositionFactory()
        ProfileFactory(position=position, user=user)

        child_user = UserFactory()
        child_position = PositionFactory(parent=position)
        ProfileFactory(position=child_position, user=child_user)
        child_user.experience_points.introduction = True
        child_user.experience_points.save()
        self.assertEqual(
            user.experience_points.children_score,
            child_user.experience_points.score)
