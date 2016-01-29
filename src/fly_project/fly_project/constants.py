from django.utils.translation import ugettext_lazy as _


GOAL_TYPE_OPTIONS = (
    (1, _('Savings')),
    (2, _('Credit')),
    (3, _('Goal')),
)

INTERVAL_OPTIONS = (
    (1, _('Weeks')),
    (2, _('Months')),
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
    (1, _('Goal')),
    (2, _('Education')),
    (3, _('Resource')),
)

DURATION_IN_MINUTES_OPTIONS = (
    (5, _('5 Minutes')),
    (30, _('30 Minutes')),
    (60, _('1 Hour')),
)

QUESTION_TYPE_OPTIONS = (
    (1, _('Multiple Choice')),
    (2, _('True / False')),
)
