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

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_fly
    """
    help = 'Populates the tables neccessary to give "py-fly" an initial start.'
    
    def handle(self, *args, **options):
        # Open up our 'xplevel.json' file and import our settings.
        with open('./api/management/commands/xplevel.json') as data_file:
            json_data = json.load(data_file)
            for json_xplevel in json_data['xplevels']:
                # Extract the JSON values
                id = int(json_xplevel['id'])
                level = int(json_xplevel['level'])
                min_xp = int(json_xplevel['min_xp'])
                max_xp = int(json_xplevel['max_xp'])
                
                # Update or Insert a new XPLevel object base on the JSON values.
                try:
                    xplevel = XPLevel.objects.get(id=id)
                    xplevel.level = level
                    xplevel.min_xp = min_xp
                    xplevel.max_xp = max_xp
                    xplevel.save()
                    print("XPLevel - Updated", id)
                except XPLevel.DoesNotExist:
                    xplevel = XPLevel.objects.create(
                        id=id,
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
                        
        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "fly_xp_levels", "primarykey": "id",},
            {"tablename": "fly_badges", "primarykey": "id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('PyFly now setup!')