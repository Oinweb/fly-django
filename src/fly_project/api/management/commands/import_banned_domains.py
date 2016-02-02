import os
import sys
import json
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from fly_project import constants
from api.models import BannedDomain

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py import_banned_ips
    """
    help = 'Populates the banned_words.'
    
    def handle(self, *args, **options):
        # Get all our bad words.
        bad_words = []
        with open('./api/management/commands/banned_domains.json') as data_file:
            json_data = json.load(data_file)
            for domain in json_data['domain_list']:
                id = domain['id']
                name = domain['name']
                reason = domain['reason']
                try:
                    ip_obj = BannedDomain.objects.get(name=name)
                    ip_obj.name = name
                    ip_obj.reason = reason
                    ip_obj.save()
                    print("BannedDomain - Updated", id)
                except BannedDomain.DoesNotExist:
                    ip_obj = BannedDomain.objects.create(
                        id=id,
                        name=name,
                        reason=reason,
                    )
                    print("BannedDomain - Inserted", id)
    
        #-----------------
        # BUGFIX: We need to make sure our keys are synchronized.
        #-----------------
        # Link: http://jesiah.net/post/23173834683/postgresql-primary-key-syncing-issues
        cursor = connection.cursor()
        
        tables_info = [
            # eCantina Tables
            {"tablename": "fly_banned_domains", "primarykey": "id",},
        ]
        for table in tables_info:
            sql = table['tablename'] + '_' + table['primarykey'] + '_seq'
            sql = 'SELECT setval(\'' + sql + '\', '
            sql += '(SELECT MAX(' + table['primarykey'] + ') FROM ' + table['tablename'] + ')+1)'
            cursor.execute(sql)
        
        # Finish Message!
        self.stdout.write('PyFly banned words imported!')
