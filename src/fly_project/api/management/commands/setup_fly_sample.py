import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants


class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_fly_sample
    """
    help = 'Populates the tables neccessary to give us a initial start for unit tests.'
    
    def handle(self, *args, **options):
        # Defensive Code: Prevent this custom command code from running if
        #                 the application is not in 'Unit Test' mode.
        is_running_unit_tests = len(sys.argv) > 1 and sys.argv[1] == 'test'
        if not is_running_unit_tests:
            self.stdout.write('Cannot run, only acceptable command in unit testing.')
            return
        
        # Get the current time.
        now = datetime.now()
