import os
import sys
import json
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants
from api.models import BannedIP

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py import_banned_ips
    """
    help = 'Populates the banned_words.'
    
    def handle(self, *args, **options):
        # Get all our bad words.
        bad_words = []
        with open('./api/management/commands/banned_ips.json') as data_file:
            json_data = json.load(data_file)
            for ip_list in json_data['ip_list']:
                id = ip_list['id']
                ip = ip_list['ip']
                print(ip)
                try:
                    ip_obj = BannedIP.objects.get(address=ip)
                    ip_obj.address = ip
                    ip_obj.save()
                    print("BannedIP - Updated", id)
                except BannedIP.DoesNotExist:
                    ip_obj = BannedIP.objects.create(
                        id=id,
                        address=ip,
                    )
                    print("BannedIP - Inserted", id)
    
        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "fly_banned_ips", "primarykey": "id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('PyFly banned words imported!')
