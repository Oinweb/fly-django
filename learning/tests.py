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
        """Verify URL resolves to Courses List page."""
        learning_url = reverse('learning')
        found = resolve(learning_url)
        self.assertEqual(found.func,views.learning_page)

    def test_url_resolves_to_course_page_view(self):
        """Verify URL resolves to Course page."""
        found = resolve('/en/course/1/')
        self.assertEqual(found.func,views.course_page)

    def test_url_resolves_to_quiz_page_view(self):
        """Verify URL resolves to Quiz start page."""
        found = resolve('/en/quiz/1/')
        self.assertEqual(found.func,views.quiz_home_page)

    def test_url_resolves_to_quiz_page_view(self):
        """Verify URL resolves to Quiz question page."""
        found = resolve('/en/quiz/1/question/1/')
        self.assertEqual(found.func,views.quiz_question_page)

    def test_url_resolves_to_quiz_page_view(self):
        """Verify URL resolves to Quiz question page."""
        found = resolve('/en/quiz/1/question/finished')
        self.assertEqual(found.func,views.quiz_final_question_page)

    def test_learning_page_returns_correct_html(self):
        """Verify course list page loads up."""
        learning_url = reverse('learning')
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(learning_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Start',response.content)

    def test_learning_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        url = reverse('learning')
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_course_page_returns_correct_html(self):
        """Verify course page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Look at course with ID #1 and make sure the proper data
        # was returned for this course.
        response = client.get('/en/course/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Finances 101',response.content)
        self.assertIn(b'Take Quiz',response.content)

    def test_course_page_security_protects(self):
        """
            Verify course page protects students from accessing course page
            if the student does not have the required prerequisites.
        """
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Look at course with ID #1 and make sure the proper data
        # was returned for this course.
        response = client.get('/en/course/5/')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Access Denied: Course prerequisites not met.',response.content)

    def test_course_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/course/1/')
        self.assertEqual(response.status_code, 302)

    def test_quiz_page_returns_correct_html(self):
        """Verify Quiz start page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Look at course with ID #1 and make sure the proper data
        # was returned for this course.
        response = client.get('/en/quiz/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Close Quiz',response.content)
        self.assertIn(b'Begin',response.content)

    def test_quiz_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/quiz/1/')
        self.assertEqual(response.status_code, 302)

    def test_quiz_question_page_returns_correct_html(self):
        """Verify Quiz start page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Simulate starting the quiz until you reach the question page
        # to verify.
        response = client.get('/en/quiz/1/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/en/quiz/1/question/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Back',response.content)
        self.assertIn(b'Next',response.content)

    def test_quiz_question_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/quiz/1/question/1/')
        self.assertEqual(response.status_code, 302)

    def test_quiz_question_page_returns_correct_html(self):
        """Verify Quiz final page loads up."""
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Simulate walking through all the questions pages until arriving
        # on the finished page to verify.
        response = client.get('/en/quiz/1/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/en/quiz/1/question/1/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/en/quiz/1/question/2/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/en/quiz/1/question/3/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/en/quiz/1/question/finished')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Quiz Finished!',response.content)
        self.assertIn(b'Score',response.content)

    def test_quiz_final_page_is_secure(self):
        """Ensure going to this page without login will be prevented."""
        client = Client()
        response = client.get('/en/quiz/1/question/finished')
        self.assertEqual(response.status_code, 302)
