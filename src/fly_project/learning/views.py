from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
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


@login_required(login_url='/authentication')
def course_page(request, course_id):
    # Fetch the Course for the id or redirect to dashboard.
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponseBadRequest(_("Course does not exist."))

    # Fetch the Quiz for the id or redirect to dashboard.
    try:
        quiz = Quiz.objects.get(course=course)
    except Quiz.DoesNotExist:
        return HttpResponseBadRequest(_("Quiz does not exist."))


    #TODO: Add defensive code to prevent course enrollment if the
    #      prerequisites where not made.


    # Fetch the EnrolledCourse for the User and if it doesn't exist then
    # create it now.
    try:
        enrolled_course = EnrolledCourse.objects.get(course=course)
    except EnrolledCourse.DoesNotExist:
        enrolled_course = EnrolledCourse.objects.create(
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
    # Fetch the Quiz for the id or error.
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return HttpResponseBadRequest(_("Quiz does not exist."))

    # Fetch the Questions for the Quiz or error.
    try:
        questions = Question.objects.filter(quiz=quiz)
    except Question.DoesNotExist:
        return HttpResponseBadRequest(_("Question does not exist."))

    # Fetch the User's Quiz Submission and if there is no Submission then
    # create it.
    try:
        submission = QuizSubmission.objects.get(quiz=quiz,user_id=request.user.id)
    except QuizSubmission.DoesNotExist:
        submission = QuizSubmission.objects.create(
            user_id=request.user.id,
            quiz=quiz,
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
    # Fetch the Questions for the Quiz or error.
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return HttpResponseBadRequest(_("Question does not exist."))
    
    # Fetch the User's Submission for this particular Question and if there
    # is no Submission for it then create it here.
    try:
        submission = QuestionSubmission.objects.get(question_id=question_id)
    except QuestionSubmission.DoesNotExist:
        submission = QuestionSubmission.objects.create(
            user_id=request.user.id,
            quiz_id=quiz_id,
            question=question,
            type=question.type,
        )

    # Fetch all the questions that belong to this Quiz.
    questions = Question.objects.filter(quiz_id=quiz_id).order_by("num")

    # Get the next and previous questions from the current.
    next = None
    previous = None
    if len(questions) == 1:
        pass
    else:
        pass

    return render(request, 'learning/quiz/question.html',{
        'settings': settings,
        'constants': constants,
        'quiz_id': int(quiz_id),
        'next': next,
        'question': question,
        'previous': previous,
        'submission': submission,
    })


def quiz_final_question_page(request, quiz_id):
    # Fetch the submitted Quiz for the id or error.
    try:
        quiz_submission = QuizSubmission.objects.get(
            quiz_id=int(quiz_id),
            user_id=request.user.id,
        )
    except QuestionSubmission.DoesNotExist:
        return HttpResponseBadRequest(_("Quiz Submission does not exist."))

    # Fetch all the submitted Questions for the particular Quiz, else error.
    try:
        question_submissions = QuestionSubmission.objects.filter(quiz=quiz_submission.quiz)
    except QuestionSubmission.DoesNotExist:
        return HttpResponseBadRequest(_("Question Submission does not exist."))

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
        enrolled_course = EnrolledCourse.objects.get(course=quiz_submission.quiz.course)
        enrolled_course.final_mark = quiz_submission.final_mark
        if quiz_submission.final_mark >= 50:
            enrolled_course.is_finished= True
        else:
            enrolled_course.is_finished = False
        enrolled_course.save()
    except EnrolledCourse.DoesNotExist:
        pass

    return render(request, 'learning/quiz/finished.html',{
        'settings': settings,
        'constants': constants,
        'quiz_id': int(quiz_id),
        'quiz_submission': quiz_submission,
        'question_submissions': question_submissions,
    })
