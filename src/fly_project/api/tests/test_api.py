from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from resources import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APITest(TestCase):
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

    def test_api_page_returns_correct_html(self):
        """Verify API page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/api/me/',response.content)
        self.assertIn(b'api/courses/',response.content)

    def test_api_banned_domains_page_returns_correct_html(self):
        """Verify API 'Banned Domains' page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/banned_domains/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'guerrillamail.com',response.content)
        self.assertIn(b'dispostable.com',response.content)
        self.assertIn(b'yopmail.com',response.content)

    def test_api_banned_ips_page_returns_correct_html(self):
        """Verify API 'Banned IPs' page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/banned_ips/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'61.49.3.254',response.content)
