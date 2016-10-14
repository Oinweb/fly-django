from django.shortcuts import render
from django.http import HttpResponse
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
        'enrollments': EnrolledCourse.objects.filter(user=request.user.id).order_by("-created"),
    })


@login_required(login_url='/authentication')
def notifications_page(request):
    return render(request, 'account/notification.html',{
        'settings': settings,
        'constants': constants,
    })


@login_required(login_url='/authentication')
def goal_history_page(request, goal_type):
    goals = []
    if int(goal_type) is constants.SAVINGS_MYGOAL_TYPE:
        try:
            goals = SavingsGoal.objects.filter(user_id=request.user.id).order_by("-created")
        except SavingsGoal.DoesNotExist:
            goals = None
    elif int(goal_type) is constants.CREDIT_MYGOAL_TYPE:
        try:
            goals = CreditGoal.objects.filter(user_id=request.user.id).order_by("-created")
        except CreditGoal.DoesNotExist:
            goals = None
    elif int(goal_type) is constants.GOAL_MYGOAL_TYPE:
        try:
            goals = FinalGoal.objects.filter(user_id=request.user.id).order_by("-created")
        except CreditGoal.DoesNotExist:
            goals = None

    return render(request, 'account/goal_history.html',{
        'settings': settings,
        'constants': constants,
        'goals': goals,
        'goal_type': int(goal_type),
    })



@login_required(login_url='/authentication')
def badges_page(request):
    return render(request, 'account/badges.html',{
        'settings': settings,
        'constants': constants,
    })

