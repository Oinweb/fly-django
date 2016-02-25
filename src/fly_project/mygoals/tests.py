from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from mygoals import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class MyGoalsTest(TestCase):
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
    
    def test_url_resolves_to_mygoals_page_view(self):
        found = resolve('/en/mygoals')
        self.assertEqual(found.func,views.mygoals_page)
    
    def test_mygoals_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/mygoals')
        self.assertEqual(response.status_code, 200)
        
        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'/en/mygoals/savings',response.content)
        self.assertIn(b'/en/mygoals/credit',response.content)
        self.assertIn(b'/en/mygoals/final',response.content)