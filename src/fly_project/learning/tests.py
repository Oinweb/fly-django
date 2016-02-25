from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from learning import views
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
    
    def test_url_resolves_to_learning_page_view(self):
        """Verify URL resolves to this app."""
        learning_url = reverse('learning')
        found = resolve(learning_url)
        self.assertEqual(found.func,views.learning_page)
    
    def test_dashboard_page_returns_correct_html(self):
        """Verify course list page loads up."""
        learning_url = reverse('learning')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(learning_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Begin Course',response.content)
