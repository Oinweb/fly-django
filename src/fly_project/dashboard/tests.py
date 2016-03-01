from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from dashboard import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class DashboardTest(TestCase):
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

    def test_url_resolves_to_dashboard_page_view(self):
        """Verify URL resolves to this app."""
        dashboard_url = reverse('dashboard')
        found = resolve(dashboard_url)
        self.assertEqual(found.func,views.dashboard_page)

    def test_dashboard_page_returns_correct_html(self):
        """Verify page loads up."""
        dashboard_url = reverse('dashboard')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'My Goals',response.content)

    def test_dashboard_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        dashboard_url = reverse('dashboard')
        client = Client()
        response = client.get(dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_page_grants_badge(self):
        """Verify a Badge is granted to User on initial load of page."""
        dashboard_url = reverse('dashboard')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        me = Me.objects.all()[:1][0]  # Fetch the only instance of 'Me' object.
        badge = Badge.objects.get(id=1)
        self.assertIn(badge,me.badges.all())
