from django.core.urlresolvers import resolve, reverse
from django.test import TestCase, Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage import views


class LandpageTest(TestCase):
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

    def tearDown(self):
        pass

    def setUp(self):
        translation.activate('en')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/en/')
        self.assertEqual(found.func,views.land_page)

    def test_home_page_returns_correct_html(self):
        parameters = {}
        client = Client()
        response = client.post(
            '/en/',
            data=parameters,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'/en/authentication',response.content)
