from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from fly_project import constants
from api.models import Course
from api.models import Quiz
from api.models import QuizSubmission


@login_required(login_url='/authentication')
def learning_page(request):
    try:
        unlocked_courses = Course.objects.filter(has_prerequisites=False).order_by("created")
    except Course.DoesNotExist:
        unlocked_courses = None

    try:
        locked_courses = Course.objects.filter(has_prerequisites=True).order_by("created")
    except Course.DoesNotExist:
        locked_courses = None

    return render(request, 'learning/course/master/view.html',{
        'settings': settings,
        'unlocked_courses': unlocked_courses,
        'locked_courses': locked_courses,
    })


@login_required(login_url='/authentication')
def course_page(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        course = None

    try:
        quiz = Quiz.objects.get(course=course)
    except Quiz.DoesNotExist:
        quiz = None

    try:
        quiz_submission = QuizSubmission.objects.get(quiz=quiz)
    except QuizSubmission.DoesNotExist:
        quiz_submission = None

    return render(request, 'learning/course/details/view.html',{
        'settings': settings,
        'constants': constants,
        'course': course,
        'quiz': quiz,
        'quiz_submission': quiz_submission,
    })


@login_required(login_url='/authentication')
def quiz_page(request, quiz_id, question_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        quiz = None
    
    return render(request, 'learning/course/details/view.html',{
        'settings': settings,
        'constants': constants,
        'quiz': quiz,
    })


