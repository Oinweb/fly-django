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

    def test_api_page(self):
        client = Client()
        response = client.get('/api/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_image_uploads_page(self):
        client = Client()
        response = client.get('/api/imageuploads/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_banned_domains_page(self):
        client = Client()
        response = client.get('/api/banned_domains/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_banned_ips_page(self):
        client = Client()
        response = client.get('/api/banned_ips/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_banned_words_page(self):
        client = Client()
        response = client.get('/api/banned_words/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_resource_links(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/resource_links/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_savings_goals(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/savings_goals/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_credit_goals(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/credit_goals/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_final_goals(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/final_goals/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_badges(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/badges/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_xplevels(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/xplevels/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_courses(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/courses/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_questions(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/questions/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_enrolled_courses(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/enrolled_courses/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_quiz_submissions(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/quiz_submissions/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_quizzes(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/quizzes/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_question_submissions(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/question_submissions/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_me(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/me/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_notifications(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/notifications/?format=json')
        self.assertEqual(response.status_code, 200)

    def test_api_shares(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/api/shares/?format=json')
        self.assertEqual(response.status_code, 200)

