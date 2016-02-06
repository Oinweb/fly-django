import datetime
from django.utils.translation import ugettext_lazy as _
from django.template import Library
from fly_project import constants
from api.models import Course
from api.models import EnrolledCourse
from api.models import Quiz
from api.models import QuizSubmission
from api.models import Question
from api.models import QuestionSubmission


register = Library()


@register.inclusion_tag('templatetags/show_goal_text.html')
def show_goal_text(goal, type):
    """
        Function will generate the appropriate Goal text message depending on 
        what 'type' of 'goal' was entered.
    """
    return {
        'constants': constants,
        'goal': goal,
        'type': int(type),
    }


@register.filter
def get_month_text(goal):
    """
        Function will return the full Month name & Year for the inputted goal.
    """
    now = datetime.datetime.now()
    
    if now.month == goal.created.month:
        return _('This Month')
    else:
        return _(goal.created.strftime("%B %Y"))


# How to get the current date and time in Python
# http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/


@register.filter
def get_goal_type_text(goal_type):
    if goal_type is constants.SAVINGS_MYGOAL_TYPE:
        return _('Savings Goal')
    elif goal_type is constants.CREDIT_MYGOAL_TYPE:
        return _('Credit Goal')
    elif goal_type is constants.GOAL_MYGOAL_TYPE:
        return _('Final Goal')
    return -1


@register.filter
def get_goal_status(goal):
    """
        1 = Success
        2 = Rejected
        3 = Locked
    """
    print(goal.is_closed)
    if goal.is_closed:
        if goal.was_accomplished:
            return 1
        else:
            return 2
    return 3
