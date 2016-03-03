from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from fly_project import settings, constants
from api.models import SavingsGoal, CreditGoal, FinalGoal


def count_days_between(dt1, dt2):
    """Function will return an integer of day numbers between two dates."""
    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days


def count_days_between_today_and(dt2):
    # Detect whether the unlocked time has elapsed and load the appropriate
    # UI associated with this.
    now = datetime.now(timezone.utc)  # Standardize date to a specific time-zone
    
    # Count how many days are left from today to the unlocked date.
    return count_days_between(now,dt2)


@login_required(login_url='/authentication')
def mygoals_page(request):
    return render(request, 'mygoals/type/view.html',{
        'settings': settings,
    })


@login_required(login_url='/authentication')
def savings_goals_page(request):
    # Check to see if we have the latest SavingsGoal set, if not then
    # create a new goal here.
    savings_goal = SavingsGoal.objects.get_latest(request.user.id)
    if not savings_goal:
        savings_goal = SavingsGoal.objects.create(user_id=request.user.id,)
    
    # Check to see if the current SavingsGoal has 'is_closed=True' which means
    # we need to create a new savings goal.
    if savings_goal.is_closed == True:
        savings_goal = SavingsGoal.objects.create(user_id=request.user.id,)
    
    # Check how many days are remaining from today to the unlock date.
    days_remaining = 99999
    if savings_goal.unlocks:
        days_remaining = count_days_between_today_and(savings_goal.unlocks)

    # CASE 1 OF 2:
    # Load the main goal settings UI.
    url = ''
    if days_remaining > 0:
        url = 'mygoals/savings/view.html'
    # CASE 2 OF 2:
    # Load the UI to handle whether the goal was set or not.
    else:
        url = 'mygoals/savings/complete.html'

    return render(request, url,{
        'settings': settings,
        'constants': constants,
        'savings_goal': savings_goal,
        'days_remaining': days_remaining,
    })


@login_required(login_url='/authentication')
def credit_goals_page(request):
    # Check to see if we have the latest CreditGoal set, if not then
    # create a new goal here.
    credit_goal = CreditGoal.objects.get_latest(request.user.id)
    if not credit_goal:
        credit_goal = CreditGoal.objects.create(user_id=request.user.id,)
    
    # Check to see if the current SavingsGoal has 'is_closed=True' which means
    # we need to create a new savings goal.
    if credit_goal.is_closed == True:
        credit_goal = CreditGoal.objects.create(user_id=request.user.id,)
    
    # Check how many days are remaining from today to the unlock date.
    days_remaining = 99999
    if credit_goal.unlocks:
        days_remaining = count_days_between_today_and(credit_goal.unlocks)

    # CASE 1 OF 2:
    # Load the main goal settings UI.
    url = ''
    if days_remaining > 0:
        url = 'mygoals/credit/view.html'
    # CASE 2 OF 2:
    # Load the UI to handle whether the goal was set or not.
    else:
        url = 'mygoals/credit/complete.html'
    
    return render(request, url,{
        'settings': settings,
        'constants': constants,
        'credit_goal': credit_goal,
        'days_remaining': days_remaining,
    })


@login_required(login_url='/authentication')
def final_goal_page(request):
    # Check to see if we have the latest FinalGoal set, if not then
    # create a new goal here.
    final_goal = FinalGoal.objects.get_latest(request.user.id)
    if not final_goal:
        final_goal = FinalGoal.objects.create(user_id=request.user.id,)

    # Check to see if the current FinalGoal has 'is_closed=True' which means
    # we need to create a new final goal.
    if final_goal.is_closed == True:
        final_goal = FinalGoal.objects.create(user_id=request.user.id,)

    # Check how many days are remaining from today to the unlock date.
    days_remaining = 99999
    if final_goal.unlocks:
        days_remaining = count_days_between_today_and(final_goal.unlocks)

    # CASE 1 OF 2:
    # Load the main goal settings UI.
    url = ''
    if days_remaining > 0:
        url = 'mygoals/final/view.html'
    # CASE 2 OF 2:
    # Load the UI to handle whether the goal was set or not.
    else:
        url = 'mygoals/final/complete.html'

    return render(request, url,{
        'settings': settings,
        'constants': constants,
        'final_goal': final_goal,
        'days_remaining': days_remaining,
    })


@login_required(login_url='/authentication')
def goal_complete_page(request, goal_type, goal_id):
    goal = None
    try:
        if goal_type == constants.SAVINGS_MYGOAL_TYPE:
            goal = SavingsGoal.objects.get(id=goal_id)
        elif goal_type == constants.CREDIT_MYGOAL_TYPE:
            goal = CreditGoal.objects.get(id=goal_id)
        elif goal_type == constants.GOAL_MYGOAL_TYPE:
            goal = FinalGoal.objects.get(id=goal_id)
    except Exception as e:
        pass

    return render(request, 'mygoals/complete/view.html',{
        'settings': settings,
        'constants': constants,
        'goal_id': int(goal_id),
        'goal_type': int(goal_type),
        'goal': goal,
    })


@login_required(login_url='/authentication')
def goal_failed_page(request, goal_type, goal_id):
    goal = None
    try:
        if goal_type == constants.SAVINGS_MYGOAL_TYPE:
            goal = SavingsGoal.objects.get(id=goal_id)
        elif goal_type == constants.CREDIT_MYGOAL_TYPE:
            goal = CreditGoal.objects.get(id=goal_id)
        elif goal_type == constants.GOAL_MYGOAL_TYPE:
            goal = FinalGoal.objects.get(id=goal_id)
    except Exception as e:
        pass


    # Evaulate the User's profile
    call_command('evaluate_me', str(request.me.id))

    return render(request, 'mygoals/failed/view.html',{
        'settings': settings,
        'constants': constants,
        'goal_id': int(goal_id),
        'goal_type': int(goal_type),
        'goal': goal,
    })


