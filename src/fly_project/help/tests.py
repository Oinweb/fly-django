from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from help import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class HelpTest(TestCase):
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

    def setUp(self):
        translation.activate('en')  # Set English

    def test_url_resolves_to_help_page_view(self):
        url = reverse('help')
        found = resolve(url)
        self.assertEqual(found.func,views.help_page)

    def test_help_page_returns_correct_html(self):
        url = reverse('help')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Contact Us',response.content)

    def test_account_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        url = reverse('help')
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
