from django.conf.urls import url, include
from api.views import imageupload
from api.views import banned_domain
from api.views import banned_ip
from api.views import banned_word
from api.views import register
from api.views import login
from api.views import goal
from api.views import badge
from api.views import xplevel
from api.views import course
from api.views import question
from api.views import enrolled_course
from api.views import quiz_submission
from api.views import question_submission
from api.views import me
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'imageuploads', imageupload.ImageUploadViewSet)
router.register(r'banned_domains', banned_domain.BannedDomainViewSet)
router.register(r'banned_ips', banned_ip.BannedIPViewSet)
router.register(r'banned_words', banned_word.BannedWordViewSet)
router.register(r'registers', register.RegisterViewSet)
router.register(r'logins', login.LoginViewSet)
router.register(r'goals', goal.GoalViewSet)
router.register(r'badges', badge.BadgeViewSet)
router.register(r'xplevels', xplevel.XPLevelViewSet)
router.register(r'courses', course.CourseViewSet)
router.register(r'questions', question.QuestionViewSet)
router.register(r'enrolled_courses', enrolled_course.EnrolledCourseViewSet)
router.register(r'quiz_submissions', quiz_submission.QuizSubmissionViewSet)
router.register(r'question_submissions', question_submission.QuestionSubmissionViewSet)
router.register(r'me', me.MeViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
]

# Used for Token Based authentication.
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]