import os
import sys
import json
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants
from api.models import XPLevel
from api.models import Badge
from api.models import Course
from api.models import Quiz
from api.models import Question
from api.models import ResourceLink


class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_fly
    """
    help = 'Populates the tables neccessary to give "py-fly" an initial start.'
    
    def handle(self, *args, **options):
        # Open up our 'xplevel.json' file and import our settings.
        with open('./api/management/commands/resources.json') as data_file:
            json_data = json.load(data_file)
            for json_resource in json_data['resources']:
                # Extract the JSON values
                id = int(json_resource['id'])
                title = json_resource['title']
                url = json_resource['url']
                type = int(json_resource['type'])
                
                # Update or Insert a new XPLevel object base on the JSON values.
                try:
                    resource = ResourceLink.objects.get(id=id)
                    resource.title = title
                    resource.url = url
                    resource.type = type
                    resource.save()
                    print("ResourceLink - Updated", id)
                except ResourceLink.DoesNotExist:
                    resource = ResourceLink.objects.create(
                        id=id,
                        title=title,
                        url=url,
                        type=type,
                    )
                    print("ResourceLink - Inserted", id)

        # Open up our 'xplevel.json' file and import our settings.
        with open('./api/management/commands/xplevels.json') as data_file:
            json_data = json.load(data_file)
            for json_xplevel in json_data['xplevels']:
                # Extract the JSON values
                id = int(json_xplevel['id'])
                title = json_xplevel['title']
                level = int(json_xplevel['level'])
                min_xp = int(json_xplevel['min_xp'])
                max_xp = int(json_xplevel['max_xp'])
                
                # Update or Insert a new XPLevel object base on the JSON values.
                try:
                    xplevel = XPLevel.objects.get(id=id)
                    xplevel.title = title
                    xplevel.level = level
                    xplevel.min_xp = min_xp
                    xplevel.max_xp = max_xp
                    xplevel.save()
                    print("XPLevel - Updated", id)
                except XPLevel.DoesNotExist:
                    xplevel = XPLevel.objects.create(
                        id=id,
                        title=title,
                        level=level,
                        min_xp=min_xp,
                        max_xp=max_xp,
                    )
                    print("XPLevel - Inserted", id)

        # Open up our 'badges.json' file and import our settings.
        with open('./api/management/commands/badges.json') as data_file:
            json_data = json.load(data_file)
            for badge in json_data['badges']:
                # Extract the JSON values
                id = int(badge['id'])
                type = int(badge['type'])
                image = badge['image']
                level = int(badge['level'])
                title = badge['title']
                description = badge['description']
                has_xp_requirement = int(badge['has_xp_requirement'])
                required_xp = int(badge['required_xp'])
                
                # Update or Insert a new Badge object base on the JSON values.
                try:
                    badge = Badge.objects.get(id=id)
                    badge.level=level
                    badge.type=type
                    badge.image=image
                    badge.title=title
                    badge.description=description
                    badge.has_xp_requirement=has_xp_requirement
                    badge.required_xp=required_xp
                    badge.save()
                    print("Badge - Updated", id)
                except Badge.DoesNotExist:
                    badge = Badge.objects.create(
                        id=id,
                        type=type,
                        image=image,
                        level=level,
                        title=title,
                        description=description,
                        has_xp_requirement=has_xp_requirement,
                        required_xp=required_xp,
                    )
                    print("Badge - Inserted", id)

        # Open up our 'courses.json' file and import our settings.
        with open('./api/management/commands/courses.json') as data_file:
            json_data = json.load(data_file)
            for json_course in json_data['courses']:
                # Extract the JSON values
                id = int(json_course['id'])
                type = int(json_course['type'])
                image = json_course['image']
                title = json_course['title']
                summary = json_course['summary']
                description = json_course['description']
                video_url = json_course['video_url']
                duration = json_course['duration']
                awarded_xp = int(json_course['awarded_xp'])
                has_prerequisites = bool(json_course['has_prerequisites'])
                prerequisites = json_course['prerequisites']
                
                # Update or Insert a new XPLevel object base on the JSON values.
                try:
                    # Update the Course.
                    course = Course.objects.get(id=id)
                    course.type=type
                    course.image=image
                    course.title=title
                    course.summary=summary
                    course.description=description
                    course.video_url=video_url
                    course.duration=duration
                    course.awarded_xp=awarded_xp
                    course.has_prerequisites=has_prerequisites
                    
                    # Update the Coure prerequisites.
                    # Step 1 of 2: Delete the existing prerequisites.
                    for prerequisite in course.prerequisites.all():
                        course.prerequisites.remove(prerequisite)
                
                    # Step 2 of 2: Add new prerequisites.
                    for prerequisite in prerequisites:
                        course.prerequisites.add(prerequisite)
                    
                    course.save()
                    print("Course - Updated", id)
                except Course.DoesNotExist:
                    # Created the Course.
                    course = Course.objects.create(
                        id=id,
                        type=type,
                        image=image,
                        title=title,
                        summary=summary,
                        description=description,
                        video_url=video_url,
                        duration=duration,
                        awarded_xp=awarded_xp,
                        has_prerequisites=has_prerequisites,
                    )
                    
                    # Populated the Course prerequisites.
                    for prerequisite in prerequisites:
                        course.prerequisites.add(prerequisite)
                    print("Course - Inserted", id)


        # Open up our 'quizzes.json' file and import our settings.
        with open('./api/management/commands/quizzes.json') as data_file:
            json_data = json.load(data_file)
            for json_quiz in json_data['quizzes']:
                # Extract the JSON values
                id = int(json_quiz['id'])
                course_id = int(json_quiz['course_id'])
                title = json_quiz['title']
                description = json_quiz['description']

                try:
                    quiz = Quiz.objects.get(id=id)
                    print("Quiz - Updated", id)
                except Quiz.DoesNotExist:
                    quiz = Quiz.objects.create(
                        id=id,
                        course_id=course_id,
                        title=title,
                        description=description,
                    )
                    print("Quiz - Inserted", id)

    
        # Open up our 'quizzes.json' file and import our settings.
        with open('./api/management/commands/questions.json') as data_file:
            json_data = json.load(data_file)
            for json_question in json_data['questions']:
                # Extract the JSON values
                id = int(json_question['id'])
                course_id = int(json_question['course_id'])
                quiz_id = int(json_question['quiz_id'])
                num = int(json_question['num'])
                text = json_question['text']
                type = int(json_question['type'])
                a = json_question['a']
                a_is_correct = bool(json_question['a_is_correct'])
                b = json_question['b']
                b_is_correct = bool(json_question['b_is_correct'])
                c = json_question['c']
                c_is_correct = bool(json_question['c_is_correct'])
                d = json_question['d']
                d_is_correct = bool(json_question['d_is_correct'])
                e = json_question['e']
                e_is_correct = bool(json_question['e_is_correct'])
                f = json_question['f']
                f_is_correct = bool(json_question['f_is_correct'])
    
                try:
                    question = Question.objects.get(id=id)
                    question.quiz_id=quiz_id
                    question.num=num
                    question.text=text
                    question.type=type
                    question.a=a
                    question.a_is_correct=a_is_correct
                    question.b=b
                    question.b_is_correct=b_is_correct
                    question.c=c
                    question.c_is_correct=c_is_correct
                    question.d=d
                    question.d_is_correct=d_is_correct
                    question.e=e
                    question.e_is_correct=e_is_correct
                    question.f=f
                    question.f_is_correct=f_is_correct
                    question.save()
                    print("Question - Updated", id)
                except Question.DoesNotExist:
                    question = Question.objects.create(
                        id=id,
                        quiz_id=quiz_id,
                        num=num,
                        text=text,
                        type=type,
                        a=a,
                        a_is_correct=a_is_correct,
                        b=b,
                        b_is_correct=b_is_correct,
                        c=c,
                        c_is_correct=c_is_correct,
                        d=d,
                        d_is_correct=d_is_correct,
                        e=e,
                        e_is_correct=e_is_correct,
                        f=f,
                        f_is_correct=f_is_correct
                    )
                    print("Question - Inserted", id)


        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "fly_xp_levels", "primarykey": "id",},
            {"tablename": "fly_badges", "primarykey": "id",},
            {"tablename": "fly_courses", "primarykey": "id",},
            {"tablename": "fly_quizzes", "primarykey": "id",},
            {"tablename": "fly_questions", "primarykey": "id",},
            {"tablename": "fly_resource_links", "primarykey": "id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('PyFly now setup!')