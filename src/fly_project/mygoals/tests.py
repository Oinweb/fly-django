from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from fly_project import constants
from mygoals import views
from api.models import Me, Badge, SavingsGoal, CreditGoal, FinalGoal


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

    def test_url_resolves_to_savings_goals_page_view(self):
        found = resolve('/en/mygoals/savings')
        self.assertEqual(found.func,views.savings_goals_page)

    def test_url_resolves_to_goal_complete_page_view(self):
        found = resolve('/en/mygoals/1/1/complete')
        self.assertEqual(found.func,views.goal_complete_page)

    def test_url_resolves_to_goal_failed_page_view(self):
        found = resolve('/en/mygoals/1/1/sorry')
        self.assertEqual(found.func,views.goal_failed_page)

    def test_url_resolves_to_credit_goals_page_view(self):
        found = resolve('/en/mygoals/credit')
        self.assertEqual(found.func,views.credit_goals_page)

    def test_url_resolves_to_final_goals_page_view(self):
        found = resolve('/en/mygoals/final')
        self.assertEqual(found.func,views.final_goal_page)

    def test_mygoals_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals')
        self.assertEqual(response.status_code, 302)

    def test_savings_goals_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals/savings')
        self.assertEqual(response.status_code, 302)

    def test_goal_complete_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals/1/1/complete')
        self.assertEqual(response.status_code, 302)

    def test_goal_failed_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals/1/1/sorry')
        self.assertEqual(response.status_code, 302)

    def test_credit_goals_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals/credit')
        self.assertEqual(response.status_code, 302)

    def test_final_goals_page_is_secure(self):
        client = Client()
        response = client.get('/en/mygoals/final')
        self.assertEqual(response.status_code, 302)

    def test_mygoals_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/mygoals')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'/en/mygoals/savings',response.content)
        self.assertIn(b'/en/mygoals/credit',response.content)
        self.assertIn(b'/en/mygoals/final',response.content)

    def test_mygoals_savings_page_returns_correct_html_for_beginning_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/mygoals/savings')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Savings',response.content)
        self.assertIn(b'Set My Goal!',response.content)

    def test_mygoals_savings_page_returns_correct_html_for_goal_is_completed(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        SavingsGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = False,
            was_accomplished = False,
            earned_xp = 25
        )
        response = client.get('/en/mygoals/savings')  # Call the URL.

        # Verify the URL results.
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Savings',response.content)
        self.assertIn(b'I want to save',response.content)
        self.assertIn(b'ajax_finish_savings_goal',response.content)

    def test_goal_complete_page_returns_correct_html_for_savings_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        SavingsGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = True,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.SAVINGS_MYGOAL_TYPE)+'/1/complete')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Congratulations',response.content)
        self.assertIn(b'You completed your goal, this is awesome!',response.content)
        self.assertIn(b'/en/mygoals/savings',response.content)

    def test_goal_failed_page_returns_correct_html_for_savings_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        SavingsGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = False,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.SAVINGS_MYGOAL_TYPE)+'/1/sorry')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Sorry',response.content)
        self.assertIn(b'Do not worry! There is always next time. Please try again!',response.content)
        self.assertIn(b'/en/mygoals/savings',response.content)

    def test_mygoals_credit_page_returns_correct_html_for_beginning_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/mygoals/credit')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Credit',response.content)
        self.assertIn(b'Set My Goal!',response.content)

    def test_mygoals_credit_page_returns_correct_html_for_goal_is_completed(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        CreditGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = False,
            was_accomplished = False,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/credit')  # Call the URL.

        # Verify the URL results.
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Credit',response.content)
        self.assertIn(b'I want to raise my credit points by ',response.content)
        self.assertIn(b'ajax_finish_credit_goal',response.content)

    def test_goal_complete_page_returns_correct_html_for_credit_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        CreditGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = True,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.CREDIT_MYGOAL_TYPE)+'/1/complete')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Congratulations',response.content)
        self.assertIn(b'You completed your goal, this is awesome!',response.content)
        self.assertIn(b'/en/mygoals/credit',response.content)

    def test_goal_failed_page_returns_correct_html_for_credit_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        CreditGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = False,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.CREDIT_MYGOAL_TYPE)+'/1/sorry')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Sorry',response.content)
        self.assertIn(b'Do not worry! There is always next time. Please try again!',response.content)
        self.assertIn(b'/en/mygoals/credit',response.content)

    def test_mygoals_final_page_returns_correct_html_for_beginning_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get('/en/mygoals/final')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Goal',response.content)
        self.assertIn(b'Set My Goal!',response.content)

    def test_mygoals_final_page_returns_correct_html_for_goal_is_completed(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        FinalGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = False,
            was_accomplished = False,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/final')  # Call the URL.

        # Verify the URL results.
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Goal',response.content)
        self.assertIn(b'I want to save',response.content)
        self.assertIn(b'ajax_finish_final_goal',response.content)

    def test_goal_complete_page_returns_correct_html_for_final_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        FinalGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = True,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.GOAL_MYGOAL_TYPE)+'/1/complete')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Congratulations',response.content)
        self.assertIn(b'You completed your goal, this is awesome!',response.content)
        self.assertIn(b'/en/mygoals/final',response.content)

    def test_goal_failed_page_returns_correct_html_for_final_goal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Create a 'SavingsGoal' which had 30 days pass by and the goal is
        # ready to be evaluated as either completed or failed.
        FinalGoal.objects.create(
            id = 1,
            user = User.objects.get(username=TEST_USER_USERNAME),
            created = '2016-02-01T18:51:20.925Z',
            is_locked = True,
            unlocks = '2016-02-01T18:51:20.925Z',
            is_closed = True,
            was_accomplished = False,
            earned_xp = 25
        )

        response = client.get('/en/mygoals/'+str(constants.GOAL_MYGOAL_TYPE)+'/1/sorry')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify the links to the three different type of Goals exist
        # in this page for the User to access.
        self.assertIn(b'Sorry',response.content)
        self.assertIn(b'Do not worry! There is always next time. Please try again!',response.content)
        self.assertIn(b'/en/mygoals/final',response.content)
