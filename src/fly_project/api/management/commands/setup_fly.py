import os
import sys
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command

class Command(BaseCommand):
    help = _('Loads all the data necessary to operate this application.')
    
    def handle(self, *args, **options):
        # The filename of all the objects to be imported.
        ordered_file_names = [
            'banned_domains.json',
            'banned_ips.json',
            'banned_words.json',
            'xplevels.json',
            'resources.json',
            'badges.json',
            'courses.json',
            'quizzes.json',
            'questions.json',
        ]
        
        # Iterate through all the filenames and load them into database.
        for file_name in ordered_file_names:
            call_command('loaddata', file_name, stdout=None)


