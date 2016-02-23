import os
import sys
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from fly_project import constants
from api.models import Badge
from api.models import Me
from api.models import XPLevel
from api.models import SavingsGoal
from api.models import CreditGoal
from api.models import FinalGoal
from api.models import Notification


class Command(BaseCommand):
    help = _('Evaluate the User\'s profile and grant reward and calculate XP.')
    
    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for id in options['id']:
            try:
                me = Me.objects.get(id=id)
                self.begin_processing(me)
            except Me.DoesNotExist:
                print("Error - No Me profile object detected for ID: "+str(id))

    def begin_processing(self, me):
        """
            Function looks at the User's profile and evaluate this account
            to determine various gamefication elements.
        """
        self.process_xp_score(me)
        self.process_xp_level_up(me)
        self.process_badges(me)

    def process_xp_score(self, me):
        """
            Function will iterate through all the Goals and sum the XP score.
        """
        xp_score = 0
        sum1 = SavingsGoal.objects.filter(user=me.user,is_closed=True).aggregate(Sum('earned_xp'))
        if sum1['earned_xp__sum']:
            me.xp = sum1['earned_xp__sum']
        
        sum2 = CreditGoal.objects.filter(user=me.user,is_closed=True).aggregate(Sum('earned_xp'))
        if sum2['earned_xp__sum']:
            me.xp = sum2['earned_xp__sum']

        sum3 = FinalGoal.objects.filter(user=me.user,is_closed=True).aggregate(Sum('earned_xp'))
        if sum3['earned_xp__sum']:
            me.xp = sum3['earned_xp__sum']
        
        me.save()

    def process_xp_level_up(self, me):
        """
            Function will select the User level based on the XP score.
        """
        # Algorithm:
        # 1. Get all the XPLevels (aka Tiers) there are in this game and arrange
        #    then in ascending order based on the Level number.
        # 2. Iterate through all the levels and only process the levels with
        #    level numbers ("num") where the User does not have.
        #     i. If the User's XP value is within the minimum and maximum of
        #        the new XPLevel then assign this new XPLevel to the User.
        #     ii. Make the User be aware of the new level.
        xp_tiers = XPLevel.objects.all().order_by("num")
        for xp_tier in xp_tiers:
            if me.xplevel.num < xp_tier.num:
                if me.xp >= xp_tier.min_xp and me.xp < xp_tier.max_xp:
                    me.xplevel = xp_tier
                    me.save()
                    self.create_level_up_notification(me, xp_tier)

    def create_level_up_notification(self,me, xp_tier):
        """
            Function will create a "New Experience Level" type of notification.
        """
        title = _("You've earned a new FLY level!")
        description = _("Congratulations! You've just leveled up your financial skills! Let your friends know, and keep up the good work!")
        Notification.objects.create(
            type=1,
            title=title,
            description=description,
            user=me.user,
            xplevel=xp_tier,
            badge=None,
        )
    
    def process_xp_level_up_badges(self, me, badge):
        """
            Function will grant the Badge to the User if it meets the requirement.
        """
        if me.xp >= badge.required_xp:
            # Grant the badge to the User.
            me.badges.add(badge)
                
            # Create a notification
            self.create_new_badge_notification(me, badge)
            print("New XP Level Badge Earned!")

    def process_courses_badges(self, me, badge):
        """
            Function will grant the Badge to the User if the specific Course
            requirements are met.
        """
        print("New Course Badge Earned!")  #TODO: Implement
    
    def process_goals_badges(self, me, badge):
        """
            Function will grant the Badge to the User if a particular goals 
            requirements have been met.
        """
        print("New Goal Badge Earned!")  #TODO: Implement
    
    def process_badges(self, me):
        """
            Function will iterate through all the badges in our application
            and evaluate whether to grant the User the particular Badge.
        """
        badges = Badge.objects.filter(has_xp_requirement=True)
        for badge in badges.all():
            if badge not in me.badges.all():
                # (1) Evaluate the Badge and User's Me profile by comparing the
                # experience points.
                self.process_xp_level_up_badges(me, badge)

                #(2) Evaluate Badge and the User's Courses to see if the User
                # should be granted a Badge.
                self.process_courses_badges(me, badge)
            
                # (3) Evaluate Badge and the User's Goals to see if the User
                # should be granted a Badge.
                self.process_goals_badges(me, badge)

    def create_new_badge_notification(self,me, badge):
        """
            Function will create a "New Badge" type of notification.
        """
        title = _("You've earned a new Badge:")+" "+badge.title
        Notification.objects.create(
            type=2,
            title=title,
            description=badge.description,
            user=me.user,
            xplevel=None,
            badge=badge,
        )