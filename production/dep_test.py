from unittest import TestCase

from production.models import Shots


class DeptTestCase(TestCase):
    def test_dep_suite(self):
        shot_queryset = Shots.objects.all()
        print(shot_queryset)