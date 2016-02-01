import os
import sys
import json
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants
from api.models import BannedWord

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_fly
    """
    help = 'Populates the banned_words.'
    
    def handle(self, *args, **options):
        # Get all our bad words.
        bad_words = []
        with open('./api/management/commands/banned_words.json') as data_file:
            bad_words_data = json.load(data_file)
            for keywords in bad_words_data['keywords']:
                bad_word = keywords['word']
                bad_words.append(bad_word)
    
        # Insert or update our database.
        for bad_word in bad_words:
            try:
                banned_word = BannedWord.objects.get(text=bad_word)
                print("Skipping", banned_word)
            except BannedWord.DoesNotExist:
                print("Creating", bad_word)
                BannedWord.objects.create(
                    text=bad_word,
                    reason='',
                )

        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "fly_banned_words", "primarykey": "id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('PyFly banned words imported!')
