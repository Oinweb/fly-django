from django.test import TestCase
from django.utils import translation
from django.core.management import call_command


class EvaluateMeTest(TestCase):
    def setUp(self):
        translation.activate('en')

    def test_run(self):
        """Verify command works"""
        call_command('setup_fly')

