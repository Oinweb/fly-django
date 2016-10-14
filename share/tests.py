from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from share import views
from api.models import Me, Badge, XPLevel, Notification


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class ShareTest(TestCase):
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

    def test_url_resolves_to_share_page_view(self):
        found = resolve('/en/share/1/')
        self.assertEqual(found.func,views.share_page)

    def test_share_page_returns_correct_html_for_custom(self):
        # Pre-Configure.
        user = User.objects.get(username=TEST_USER_USERNAME)
        Notification.objects.create(
            id=1,
            type=3,
            user=user,
            title="test 123",
            description="test 123456789",
        )

        # Login and run test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Test & Verify
        response = client.get('/en/share/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
#        self.assertIn(b'Social Media',response.content)
#        self.assertIn(b'Blogs',response.content)
#        self.assertIn(b'Other Cool Apps',response.content)

    def test_share_page_returns_correct_html_for_badge(self):
        # Pre-Configure.
        user = User.objects.get(username=TEST_USER_USERNAME)
        badge = Badge.objects.get(id=1)
        Notification.objects.create(
            id=1,
            type=2,
            user=user,
            title="test 123",
            description="test 123456789",
            badge=badge,
        )
            
        # Login and run test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Test & Verify
        response = client.get('/en/share/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
#        self.assertIn(b'Social Media',response.content)
#        self.assertIn(b'Blogs',response.content)
#        self.assertIn(b'Other Cool Apps',response.content)

    def test_share_page_returns_correct_html_for_xplevel(self):
        # Pre-Configure.
        user = User.objects.get(username=TEST_USER_USERNAME)
        xplevel = XPLevel.objects.get(id=1)
        Notification.objects.create(
            id=1,
            type=1,
            user=user,
            title="test 123",
            description="test 123456789",
            xplevel=xplevel,
        )
            
        # Login and run test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Test & Verify
        response = client.get('/en/share/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
#        self.assertIn(b'Social Media',response.content)
#        self.assertIn(b'Blogs',response.content)
#        self.assertIn(b'Other Cool Apps',response.content)