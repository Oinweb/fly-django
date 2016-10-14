import os
import sys
import json
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fly_project import constants
from api.models import QuizSubmission
from api.models import QuestionSubmission


class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py evaluate_quiz {{ quiz_submission_id }}
    """
    help = _('Command will mark and score the User\'s submitted quiz.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        # Process all the Quizzes that are inputted into this Command.
        for id in options['id']:
            try:
                submission = QuizSubmission.objects.get(id=id)
                self.begin_processing(submission)
            except QuizSubmission.DoesNotExist:
                pass

    def begin_processing(self, submission):
        """
            Function will load up the Quiz Submission and iterate through all
            Question Submissions and evaluate them for being either correct
            or wrong and then assign a mark to them.
        """
        # Step 1: Fetch all the submitted Questions for this Quiz.
        try:
            question_submissions = QuestionSubmission.objects.filter(
                quiz=submission.quiz,
                user=submission.user,
            )
        except QuestionSubmission.DoesNotExist:
            question_submissions = None
        

        # Step 2: Iterate through all the submitted Questions and mark them
        #         either right or wrong depending on the correct answer.
        for question_submission in question_submissions.all():
            is_right = True
            question_answer = question_submission.question

            # Step 3: If the question is 'Open-ended' then simply give the
            #         student the mark and finish this function, else then
            #         evaluate the quiz question.
            if question_submission.type == 1:
                question_submission.mark = 1
            
            else:
                if question_submission.a is not question_answer.a_is_correct:
                    is_right = False
                if question_submission.b is not question_answer.b_is_correct:
                    is_right = False
                if question_submission.c is not question_answer.c_is_correct:
                    is_right = False
                if question_submission.d is not question_answer.d_is_correct:
                    is_right = False
                if question_submission.e is not question_answer.e_is_correct:
                    is_right = False
                if question_submission.f is not question_answer.f_is_correct:
                    is_right = False

                if is_right:
                    question_submission.mark = 1
                else:
                    question_submission.mark = 0
                        
            question_submission.save()

        # Step 4: Iterate through all the submitted Questions and perform a
        # total mark tally of the Quiz and then mark the Quiz either a success
        # or a failure.
        total_mark = 0
        actual_mark = 0
        for question_submission in question_submissions.all():
            total_mark += 1
            actual_mark += question_submission.mark
        final_mark = (actual_mark / total_mark) * 100

        submission.final_mark = final_mark
        submission.save()
