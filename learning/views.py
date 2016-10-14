from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from fly_project import settings
from fly_project import constants
from api.models import Course
from api.models import EnrolledCourse
from api.models import Quiz
from api.models import QuizSubmission
from api.models import Question
from api.models import QuestionSubmission


@login_required(login_url='/authentication')
def learning_page(request):
    try:
        unlocked_courses = Course.objects.filter(has_prerequisites=False).order_by("created")
    except Course.DoesNotExist:
        return HttpResponseBadRequest(_("No courses where found."))

    try:
        locked_courses = Course.objects.filter(has_prerequisites=True).order_by("created")
    except Course.DoesNotExist:
        return HttpResponseBadRequest(_("No locked courses where found."))

    return render(request, 'learning/course/master/view.html',{
        'settings': settings,
        'unlocked_courses': unlocked_courses,
        'locked_courses': locked_courses,
    })


def has_course_prerequisites(course, enrollments):
    """Function will return True/False depending on if pre-requisites are met."""
    if course.has_prerequisites == False:
        return True

    prerequisite_count = 0
    for prerequisite in course.prerequisites.all():
        for enrollment in enrollments.all():
            if enrollment.course == prerequisite:
                if enrollment.is_finished:
                    prerequisite_count += 1

    return prerequisite_count == len(course.prerequisites.all())


@login_required(login_url='/authentication')
def course_page(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, course=course)

    # Security: Prevent course access if pre-requisites not met.
    if has_course_prerequisites(course, request.me.courses.all()) == False:
        return HttpResponseBadRequest(_("Access Denied: Course prerequisites not met."))

    # Fetch the EnrolledCourse for the User and if it doesn't exist then
    # create it now.
    enrolled_course, created = EnrolledCourse.objects.get_or_create(
        user_id=request.user.id,
        course=course,
    )

    return render(request, 'learning/course/details/view.html',{
        'settings': settings,
        'constants': constants,
        'course': course,
        'quiz': quiz,
        'enrolled_course': enrolled_course,
    })


@login_required(login_url='/authentication')
def quiz_home_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = get_list_or_404(Question, quiz=quiz)

    # Fetch the User's Quiz Submission and if there is no Submission then
    # create it.
    submission, created  = QuizSubmission.objects.get_or_create(
        quiz=quiz,
        user_id=request.user.id,
        course=quiz.course,
    )

    # Iterate to any existing submitted Questions and reset the selected
    # values so the Quiz is brand new.
    question_submissions = QuestionSubmission.objects.filter(quiz=quiz)
    for question_submission in question_submissions.all():
        question_submission.a = False
        question_submission.b = False
        question_submission.c = False
        question_submission.d = False
        question_submission.e = False
        question_submission.f = False
        question_submission.save()

    return render(request, 'learning/quiz/start.html',{
        'settings': settings,
        'constants': constants,
        'quiz': quiz,
        'questions': questions,
        'submission': submission,
    })


@login_required(login_url='/authentication')
def quiz_question_page(request, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Fetch the User's Submission for this particular Question and if there
    # is no Submission for it then create it here.
    submission, created  = QuestionSubmission.objects.get_or_create(
        user_id=request.user.id,
        quiz_id=quiz_id,
        question=question,
        type=question.type,
    )

    # Fetch all the questions that belong to this Quiz.
    questions = Question.objects.filter(quiz_id=quiz_id).order_by("num")

    # Get "NEXT"
    next = None
    if len(questions) > 1:
        for current_question in questions.all():
            # Detect the previous question.
            if current_question.num > question.num:
                next = current_question
                break

    # Get "PREVIOUS"
    previous = None
    if len(questions) > 1:
        for current_question in questions.all():
            if (question.num - 1) == current_question.num:
                previous = current_question
                break

    return render(request, 'learning/quiz/question.html',{
        'settings': settings,
        'constants': constants,
        'quiz_id': int(quiz_id),
        'next': next,
        'question': question,
        'previous': previous,
        'submission': submission,
    })


@login_required(login_url='/authentication')
def quiz_final_question_page(request, quiz_id):
    quiz_submission = get_object_or_404(QuizSubmission,  quiz_id=int(quiz_id), user_id=request.user.id,)
    question_submissions = get_list_or_404(QuestionSubmission, quiz=quiz_submission.quiz)

    # Run the Command for evaluating the Quiz and tallying up the marks.
    call_command('evaluate_quiz',str(quiz_submission.id))

    # Fetch again the newly evaluated submitted Quiz.
    quiz_submission = QuizSubmission.objects.get(
        quiz_id=int(quiz_id),
        user_id=request.user.id,
    )

    # Fetch the EnrolledCourse for the User and evaluate it based off the
    # submitted Quiz.
    try:
        enrolled_course = EnrolledCourse.objects.get(
            course=quiz_submission.quiz.course,
            user_id=request.user.id,
        )
        enrolled_course.final_mark = quiz_submission.final_mark
        if quiz_submission.final_mark >= 50:
            enrolled_course.is_finished= True
        else:
            enrolled_course.is_finished = False
        enrolled_course.save()

        request.me.courses.add(enrolled_course)
    except EnrolledCourse.DoesNotExist:
        pass

    return render(request, 'learning/quiz/finished.html',{
        'settings': settings,
        'constants': constants,
        'quiz_id': int(quiz_id),
        'quiz_submission': quiz_submission,
        'question_submissions': question_submissions,
    })
