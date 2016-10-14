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