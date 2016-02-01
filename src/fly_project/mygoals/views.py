from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from fly_project import constants
from api.models import SavingsGoal
from api.models import CreditGoal
from api.models import FinalGoal
from rest_framework.authtoken.models import Token


@login_required(login_url='/authentication')
def mygoals_page(request):
    
    savings_goal = SavingsGoal.objects.get_latest(request.user.id)
    credit_goal = CreditGoal.objects.get_latest(request.user.id)
    final_goal = FinalGoal.objects.get_latest(request.user.id)
    
    if not savings_goal:
        print("Creating New Savings Goal")
        savings_goal = SavingsGoal.objects.create(
            user_id=request.user.id,
        )
    if not credit_goal:
        print("Creating New Credit Goal")
        credit_goal = CreditGoal.objects.create(
            user_id=request.user.id,
        )
    if not final_goal:
        print("Creating New Final Goal")
        credit_goal = FinalGoal.objects.create(
            user_id=request.user.id,
        )

    return render(request, 'mygoals/view.html',{
        'settings': settings,
        'constants': constants,
        'savings_goal': savings_goal,
        'credit_goal': credit_goal,
        'final_goal': final_goal,
    })

#SAVINGS_MYGOAL_TYPE = 1
#CREDIT_MYGOAL_TYPE = 2
#GOAL_MYGOAL_TYPE = 3
