from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.management import call_command
from api.models import Me, Badge, XPLevel


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class EvaluateMeTest(TestCase):
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        'xplevels.json',
        'resources.json',
        'badges.json',
        'courses.json',
        'quizzes.json',
        'questions.json',
    ]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()
        Me.objects.create(
            user=user,
            xplevel=XPLevel.objects.get_or_create_for_level_one(),
        )

    def setUp(self):
        translation.activate('en')  # Set English


    def test_run_for_missing_user(self):
        """Verify command works for user"""
        call_command('evaluate_me', str(666))


    def test_run_for_existing_user(self):
        """Verify command works for user"""
        call_command('evaluate_me', str(1))

