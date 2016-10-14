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
from api.models import Course
from api.models import EnrolledCourse
from api.models import Share


class Command(BaseCommand):
    help = _('Evaluate the User\'s profile and grant reward and calculate XP.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for id in options['id']:
            try:
                me = Me.objects.get(id=id)
                self.begin_processing(me)
            except Me.DoesNotExist:
                print(_("Error - No Me profile object detected for ID: ")+str(id))

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
        if badge.has_xp_requirement:
            if me.xp >= badge.required_xp:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)

    def process_badge_per_course(self, me, badge, course_id):
        # Lookup the particular 'course_id' which is succesfully completed.
        try:
            completed_course = EnrolledCourse.objects.get(
                course_id=course_id,
                user=me.user,
                is_finished=True,
            )

            # If the User does not have a record of this course then add it
            # to the User's profile and grant the badge and make notification.
            if completed_course not in me.courses.all():
                print("Badge",badge.id)
                me.courses.add(completed_course)
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
                
        except EnrolledCourse.DoesNotExist:
            pass

    def process_badge_for_social(self, me, badge, shares):
        if shares.count() > 0:
            me.badges.add(badge)
            self.create_new_badge_notification(me, badge)
    
    def process_courses_badges(self, me, badge):
        """
            Function will grant the Badge to the User if the specific Course
            requirements are met.
        """
        # Thanks for letting your friends know! - #12
        shares = Share.objects.filter(user=me.user)
        if badge.id == 12:
            self.process_badge_for_social(me, badge, shares)

        # Completed Finances 101 - #13
        if badge.id == 13:
            self.process_badge_per_course(me, badge, 1)

        # Completed Finances II - #14
        if badge.id == 14:
            self.process_badge_per_course(me, badge, 4)

        # Completed Saving & Budgeting 101 - #15
        if badge.id == 15:
            self.process_badge_per_course(me, badge, 2)

        # Saving & Budgeting II - #16
        if badge.id == 16:
            self.process_badge_per_course(me, badge, 5)

        # Completed Credit Score 101 - #17
        if badge.id == 17:
            self.process_badge_per_course(me, badge, 3)

        # Completed Credit Score II - #18
        if badge.id == 18:
            self.process_badge_per_course(me, badge, 6)

        # First Course - #11
        if badge.id == 11:
            if me.courses.count() == 1:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)

    def process_badge_21(self, me, badge):
        savings_goals_failure_count = SavingsGoal.objects.filter(
            user=me.user,
            was_accomplished = False,
            is_closed = True,
        ).count()
        credit_goals_failure_count = CreditGoal.objects.filter(
            user=me.user,
            was_accomplished = False,
            is_closed = True,
        ).count()
        final_goals_failure_count = FinalGoal.objects.filter(
            user=me.user,
            was_accomplished = False,
            is_closed = True,
        ).count()
        
        if savings_goals_failure_count or credit_goals_failure_count or final_goals_failure_count:
            me.badges.add(badge)
            self.create_new_badge_notification(me, badge)

    def process_goals_badges(self, me, badge):
        """
            Function will grant the Badge to the User if a particular goals
            requirements have been met.
        """
        # Goal Sharing - #20
        #TODO: Implement
        
        # Fetch all the goals accomplished for this user which we will use
        # to evaluate handing out Badges to if certain criteria are met.
        savings_goals_count = SavingsGoal.objects.filter(
            user=me.user,
            was_accomplished = True,
            is_closed = True,
        ).count()
        credit_goals_count = CreditGoal.objects.filter(
            user=me.user,
            was_accomplished = True,
            is_closed = True,
        ).count()
        final_goals_count = FinalGoal.objects.filter(
            user=me.user,
            was_accomplished = True,
            is_closed = True,
        ).count()
        
        # First goal achieved - #19
        if badge.id == 19:
            if savings_goals_count or credit_goals_count or final_goals_count:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
        
        # First goal failed - #21
        if badge.id == 21:
            self.process_badge_21(me, badge)
        
        # First savings goal achieved - #22
        if badge.id == 22:
            if savings_goals_count:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
        
        # First credit goal achieved - #23
        if badge.id == 23:
            if credit_goals_count:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
        
        # First big goal achieved - #24
        if badge.id == 24:
            if final_goals_count:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
    
        # Savings champ - #25
        if badge.id == 25:
            if savings_goals_count >= 3:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)
    
        # Credit score champ - #26
        if badge.id == 26:
            if credit_goals_count >= 3:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)

        # Big saver! - #27
        if badge.id == 27:
            if final_goals_count >= 3:
                me.badges.add(badge)
                self.create_new_badge_notification(me, badge)

    def process_badges(self, me):
        """
            Function will iterate through all the badges in our application
            and evaluate whether to grant the User the particular Badge.
        """
        badges = Badge.objects.all()
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

    def create_new_badge_notification(self, me, badge):
        """Function will create a "New Badge" type of notification."""
        title = _("You've earned a new Badge:")+" "+badge.title
        Notification.objects.create(
            type=2,
            title=title,
            description=badge.description,
            user=me.user,
            xplevel=None,
            badge=badge,
        )
