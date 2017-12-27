from django.test import TestCase

from ...factories import (
    LCFactory,
    PositionFactory)


class PositionTest(TestCase):

    def test_string_representation(self):
        LCFactory.create()
        position = PositionFactory.create(parent=None)

        self.assertEqual(
            position.__str__(), '%s %s' % (position.type, position.title))

        sub_position = PositionFactory(parent=position)
        self.assertEqual(
            sub_position.__str__(), '%s > %s %s' % (
                sub_position.parent.__str__(),
                sub_position.type,
                sub_position.title))
