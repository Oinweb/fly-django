from django.utils.translation import ugettext_lazy as _


SAVINGS_MYGOAL_TYPE = 1
CREDIT_MYGOAL_TYPE = 2
GOAL_MYGOAL_TYPE = 3
GOAL_TYPE_OPTIONS = (
    (SAVINGS_MYGOAL_TYPE, _('Savings')),
    (CREDIT_MYGOAL_TYPE, _('Credit')),
    (GOAL_MYGOAL_TYPE, _('Goal')),
)


WEEKS_TYPE = 1
MONTHS_TYPE = 2
INTERVAL_OPTIONS = (
    (WEEKS_TYPE, _('Weeks')),
    (MONTHS_TYPE, _('Months')),
)

FOR_WANT_OPTIONS = (
    (1, _('House')),
    (2, _('Business')),
    (3, _('Vacation')),
    (4, _('Retirement')),
    (5, _('General Savings')),
    (6, _('Other')),
)

BADGE_TYPE_OPTIONS = (
    (1, _('Badge')),
    (2, _('Goal Badge')),
    (3, _('Education Badge')),
    (4, _('Resource Badge')),
)

DURATION_IN_MINUTES_OPTIONS = (
    (5, _('5 Minutes')),
    (30, _('30 Minutes')),
    (60, _('1 Hour')),
)

QUESTION_TYPE_OPTIONS = (
    (1, _('Open-Ended')),
    (2, _('Partial')),
    (3, _('All-or-None')),
)

RESOURCE_TYPE_OPTIONS = (
    (1, _('Social Media')),
    (2, _('Blogs')),
    (3, _('Other Cool Apps')),
)

NOTIFICATION_TYPE_OPTIONS = (
    (1, _('Level Up Notifiction')),
    (2, _('New Badge Notification')),
    (3, _('Custom Notification')),
)


SHARE_TYPE_OPTIONS = (
    (1, _('Level Up Share')),
    (2, _('New Badge Share')),
    (3, _('Custom Share')),
)