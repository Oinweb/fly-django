import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage import views


class LandpageTest(TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        pass

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
        self.assertIn(b'Generic Login',response.content)
