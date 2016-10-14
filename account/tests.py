from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from account import views
from api.models import Me, Badge


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class AccountTest(TestCase):
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

    def test_url_resolves_to_account_page_view(self):
        url = reverse('account')
        found = resolve(url)
        self.assertEqual(found.func,views.account_page)

    def test_url_resolves_to_notifications_page_view(self):
        url = reverse('notifications')
        found = resolve(url)
        self.assertEqual(found.func,views.notifications_page)

    def test_url_resolves_to_goal_history_page_view(self):
        found = resolve('/en/goal_history/1/')
        self.assertEqual(found.func,views.goal_history_page)

    def test_url_resolves_to_badges_page_view(self):
        found = resolve('/en/badges')
        self.assertEqual(found.func,views.badges_page)

    def test_account_page_returns_correct_html(self):
        url = reverse('account')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'User Info',response.content)
        self.assertIn(b'Current Goals',response.content)
        self.assertIn(b'Delete Account',response.content)

    def test_account_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        url = reverse('account')
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_notifications_page_returns_correct_html(self):
        url = reverse('notifications')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Notifications',response.content)
        self.assertIn(b'Save Changes',response.content)

    def test_notifications_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        url = reverse('notifications')
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_goal_history_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/goal_history/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'History',response.content)

    def test_goal_history_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/goal_history/1/')
        self.assertEqual(response.status_code, 302)

    def test_badges_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/badges')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Badges',response.content)

    def test_badges_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/badges')
        self.assertEqual(response.status_code, 302)
