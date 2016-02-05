from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from fly_project import constants
from api.models import SavingsGoal
from api.models import CreditGoal
from api.models import FinalGoal
from api.models import Course
from api.models import EnrolledCourse
from api.models import Quiz
from api.models import QuizSubmission
from api.models import Question
from api.models import QuestionSubmission


@login_required(login_url='/authentication')
def account_page(request):
    return render(request, 'account/profile.html',{
        'settings': settings,
        'constants': constants,
        'savings_goal': SavingsGoal.objects.get_latest(request.user.id),
        'credit_goal': CreditGoal.objects.get_latest(request.user.id),
        'final_goal': FinalGoal.objects.get_latest(request.user.id),
        'enrollments': EnrolledCourse.objects.filter(user=request.user.id),
    })


@login_required(login_url='/authentication')
def notifications_page(request):
    return render(request, 'account/notification.html',{
        'settings': settings,
        'constants': constants,
    })