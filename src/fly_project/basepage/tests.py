from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from basepage import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class BasePageTest(TestCase):
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

    def test_url_resolves_to_robots_page_view(self):
        found = resolve('/robots.txt')
        self.assertEqual(found.func,views.robots_txt_page)

    def test_url_resolves_to_humans_page_view(self):
        found = resolve('/humans.txt')
        self.assertEqual(found.func,views.humans_txt_page)

    def test_url_resolves_to_ssl_page_view(self):
        found = resolve('/38657648AF65578D3AD846C1DB9497C8.txt')
        self.assertEqual(found.func,views.ssl_txt_page)

    def test_robots_page_returns_correct_html(self):
        client = Client()
        response = client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Disallow: /static',response.content)

    def test_humans_page_returns_correct_html(self):
        client = Client()
        response = client.get('/humans.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Bartlomiej Mika',response.content)
        self.assertIn(b'Chad Smith',response.content)
        self.assertIn(b'Rodolfo Martinez',response.content)

    def test_ssl_page_returns_correct_html(self):
        client = Client()
        response = client.get('/38657648AF65578D3AD846C1DB9497C8.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'comodoca.com',response.content)
