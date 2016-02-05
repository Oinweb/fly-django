from django.template import Library
from api.models import Course
from api.models import EnrolledCourse
from api.models import Quiz
from api.models import QuizSubmission
from api.models import Question
from api.models import QuestionSubmission


register = Library()


@register.filter
def has_completed(user,course):
    """
        Function will return True/False depending on whether the enrolled
        course is finished successfully by the user.
    """
    try:
        enrollment = EnrolledCourse.objects.get(user=user,course=course)
    except EnrolledCourse.DoesNotExist:
        return False

    return enrollment.is_finished


@register.filter
def has_prerequisites(user,course):
    """
        Function will return True/False depending on whether all the 
        prerequisites are met for the particular course & user.
    """
    try:
        enrollments = EnrolledCourse.objects.filter(user=user)
    except EnrolledCourse.DoesNotExist:
        enrollments = None

    prerequisite_count = 0
    for prerequisite in course.prerequisites.all():
        for enrollment in enrollments.all():
            if enrollment.course == prerequisite:
                if enrollment.is_finished:
                    prerequisite_count += 1

    return prerequisite_count == len(course.prerequisites.all())