import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants
from api.models import XPLevel

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_fly
    """
    help = 'Populates the tables neccessary to give "py-fly" an initial start.'
    
    def handle(self, *args, **options):
        pass
#        #-----------------
#        # BUGFIX: We need to make sure our keys are synchronized.
#        #-----------------
#        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
#        cursor = connection.cursor()
#        
#        tables_info = [
#            # eCantina Tables
#            {"tablename": "fly_xp_levels", "primarykey": "id",},
#        ]
#        for table in tables_info:
#            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
#            sql = 'SELECT setval(\'' + sql + '\', '
#            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
#            cursor.execute(sql)
#        
#        # Finish Message!
#        self.stdout.write('PyFly now setup!')