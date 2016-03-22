from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class AuthenticationTest(TestCase):
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

    def test_url_resolves_to_authentication_page_view(self):
        url = reverse('authentication')
        found = resolve(url)
        self.assertEqual(found.func,views.authentication_page)

    def test_url_resolves_to_login_page_view(self):
        url = reverse('login')
        found = resolve(url)
        self.assertEqual(found.func,views.login_page)

    def test_url_resolves_to_register_page_view(self):
        url = reverse('register')
        found = resolve(url)
        self.assertEqual(found.func,views.register_page)

    def test_authentication_page_returns_correct_html(self):
        url = reverse('authentication')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Facebook',response.content)
        self.assertIn(b'Twitter',response.content)
        self.assertIn(b'Google',response.content)
        self.assertIn(b'E-Mail Login',response.content)
        self.assertIn(b'Register',response.content)

    def test_login_page_returns_correct_html(self):
        url = reverse('login')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Create Account',response.content)
        self.assertIn(b'Close',response.content)
        self.assertIn(b'Login',response.content)


    def test_register_page_returns_correct_html(self):
        url = reverse('register')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Login',response.content)
        self.assertIn(b'Close',response.content)
        self.assertIn(b'Register',response.content)
