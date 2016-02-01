from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from fly_project import constants
from api.models import Goal
from rest_framework.authtoken.models import Token


@login_required(login_url='/authentication')
def mygoals_page(request):
    
    savings_goal = Goal.objects.get_latest_savings_goal(request.user.id)
    credit_goal = Goal.objects.get_latest_credit_goal(request.user.id)
    final_goal = Goal.objects.get_latest_final_goal(request.user.id)
    
    if not savings_goal:
        print("Creating New Savings Goal")
        savings_goal = Goal.objects.create(
            user_id=request.user.id,
            type=constants.SAVINGS_MYGOAL_TYPE,
        )
    if not credit_goal:
        print("Creating New Credit Goal")
        credit_goal = Goal.objects.create(
            user_id=request.user.id,
            type=constants.CREDIT_MYGOAL_TYPE,
        )
    if not final_goal:
        print("Creating New Final Goal")
        credit_goal = Goal.objects.create(
            user_id=request.user.id,
            type=constants.GOAL_MYGOAL_TYPE,
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
