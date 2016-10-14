import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from fly_project import constants


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# http://stackoverflow.com/questions/14838128/django-rest-framework-token-authentication


class BannedDomain(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'fly_banned_domains'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class BannedIP(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('address',)
        db_table = 'fly_banned_ips'

    id = models.AutoField(primary_key=True)
    address = models.GenericIPAddressField(db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    def __str__(self):
        return str(self.address)


class BannedWord(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('text',)
        db_table = 'fly_banned_words'

    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    def __str__(self):
        return str(self.text)


class ImageUpload(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_image_uploads'

    upload_id = models.AutoField(primary_key=True)
    upload_date = models.DateField(auto_now=True, null=True)
    image = models.ImageField(upload_to='upload', null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True,)

    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(ImageUpload, self).delete(*args, **kwargs) # Call the "real" delete() method

    def __str__(self):
        return str(self.upload_id)


class ResourceLink(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_resource_links'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=127,)
    url = models.URLField()
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.RESOURCE_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )

    def __str__(self):
        return str(self.url)


class Goal(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, db_index=True,)

    # Variable to be used to save the initial date this goal was created on.
    created = models.DateTimeField(auto_now_add=True, db_index=True,)

    # Variable controls whether the User has set the Goal and will wait
    # 30 days before this Goal will unlock.
    is_locked = models.BooleanField(default=False)

    # Variable allows the client to find out the goal type
    # through an ajax request
    goal_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        blank=True,
        default=0,
        db_index=True,
    )

    # Variable controls when this particular goal can be closed. Closure
    # involves modifying 'is_closed' and 'earned_xp' values.
    unlocks = models.DateTimeField(null=True, blank=True)

    # Variable controls whether this particular goal was finished and thus
    # cannot be modified after it was closed.
    is_closed = models.BooleanField(default=False, db_index=True,)

    # When 'is_closed=True' variable was set, this variable controls whether
    # the User has actually finished this goal with success or not.
    was_accomplished = models.BooleanField(default=False, db_index=True)

    # When 'is_closed=True' variable was set, this variable controls what
    # amount of experience points where earned for accomplishing it.
    earned_xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        default=0,
    )

    def __str__(self):
        return str(self.id)


class SavingsGoalManager(models.Manager):
    def get_latest(self, user_id):
        try:
            return SavingsGoal.objects.filter(user_id=user_id).latest('created')
        except SavingsGoal.DoesNotExist:
            return None


class SavingsGoal(Goal):
    class Meta:
        app_label = 'api'
        db_table = 'fly_savings_goals'

    objects = SavingsGoalManager()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    times = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        default=0,
    )
    period = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=constants.INTERVAL_OPTIONS,
        default=1,
    )


class OrderedSavingsGoal(SavingsGoal):
    class Meta:
        ordering = ('-created',)
        proxy = True


class CreditGoalManager(models.Manager):
    def get_latest(self, user_id):
        try:
            return CreditGoal.objects.filter(user_id=user_id).latest('created')
        except CreditGoal.DoesNotExist:
            return None


class CreditGoal(Goal):
    class Meta:
        app_label = 'api'
        db_table = 'fly_credit_goals'

    objects = CreditGoalManager()
    points = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(850)],
        default=0,
    )
    times = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        default=0,
    )
    period = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=constants.INTERVAL_OPTIONS,
        default=1,
    )


class OrderedCreditGoal(CreditGoal):
    class Meta:
        ordering = ('-created',)
        proxy = True


class FinalGoalManager(models.Manager):
    def get_latest(self, user_id):
        try:
            return FinalGoal.objects.filter(user_id=user_id,).latest('created')
        except FinalGoal.DoesNotExist:
            return None


class FinalGoal(Goal):
    class Meta:
        app_label = 'api'
        db_table = 'fly_final_goals'

    objects = FinalGoalManager()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    for_want = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        choices=constants.FOR_WANT_OPTIONS,
        default=1,
    )
    for_other_want = models.CharField(max_length=63, default='', null=True, blank=True)


class OrderedFinalGoal(FinalGoal):
    class Meta:
        ordering = ('-created',)
        proxy = True


class Badge(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_badges'

    id = models.AutoField(primary_key=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        choices=constants.BADGE_TYPE_OPTIONS,
        default=1,
    )
    icon = models.CharField(max_length=31, null=True, blank=True)
    colour = models.CharField(max_length=31, null=True, blank=True)
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        default=1,
    )
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)
    has_xp_requirement = models.BooleanField(default=True, blank=True,)
    required_xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
    )

    def __str__(self):
        return str(self.id)


class XPLevelManager(models.Manager):
    def get_or_create_for_level_one(self):
        """
            Function will lookup
        """
        try:
            return XPLevel.objects.get(num=1)
        except XPLevel.DoesNotExist:
            return self.create(
                num=1,
                min_xp=0,
                max_xp=25,
            )


class XPLevel(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_xp_levels'

    objects = XPLevelManager()
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=31, null=True, blank=True)
    num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        choices=constants.DURATION_IN_MINUTES_OPTIONS,
        default=1,
    )
    min_xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        default=0,
    )
    max_xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        default=25,
    )

    def __str__(self):
        return str(self.id)


class CourseManager(models.Manager):
    def get_by_id_or_none(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            return None


class Course(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_courses'

    objects = CourseManager()
    id = models.AutoField(primary_key=True, db_index=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.GOAL_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    image = models.CharField(max_length=63, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True,)
    title = models.CharField(max_length=63, null=True, blank=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(60)],
        choices=constants.DURATION_IN_MINUTES_OPTIONS,
        default=5,
    )
    awarded_xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        default=1,
    )
    has_prerequisites = models.BooleanField(default=False,db_index=True,)
    prerequisites = models.ManyToManyField("self", blank=True,)

    def __str__(self):
        return str(self.id)


class OrderedCourse(Course):
    class Meta:
        ordering = ('created',)
        proxy = True


class Quiz(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_quizzes'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, db_index=True,)
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Question(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_questions'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, db_index=True,)
    num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        default=1,
    )
    text = models.CharField(max_length=511, null=True, blank=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.QUESTION_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    a = models.CharField(max_length=255, null=True, blank=True,)
    a_is_correct = models.BooleanField(default=False)
    b = models.CharField(max_length=255, null=True, blank=True,)
    b_is_correct = models.BooleanField(default=False)
    c = models.CharField(max_length=255, null=True, blank=True)
    c_is_correct = models.BooleanField(default=False)
    d = models.CharField(max_length=255, null=True, blank=True)
    d_is_correct = models.BooleanField(default=False)
    e = models.CharField(max_length=255, null=True, blank=True)
    e_is_correct = models.BooleanField(default=False)
    f = models.CharField(max_length=255, null=True, blank=True)
    f_is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class OrderedQuestion(Question):
    class Meta:
        ordering = ('num',)
        proxy = True


class EnrolledCourse(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_enrolled_courses'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_index=True,)
    course = models.ForeignKey(Course)
    finished = models.DateTimeField(null=True, blank=True,)
    is_finished = models.BooleanField(default=False)
    final_mark = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100),],
        default=0,
    )

    def __str__(self):
        return str(self.id)


class QuizSubmission(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_quiz_submissions'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course,)
    user = models.ForeignKey(User, db_index=True,)
    quiz = models.ForeignKey(Quiz, db_index=True,)
    finished = models.DateTimeField(null=True, blank=True,)
    is_finished = models.BooleanField(default=False)
    final_mark = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100),],
        default=0,
    )

    def __str__(self):
        return str(self.id)


class QuestionSubmission(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_question_submissions'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_index=True,)
    question = models.ForeignKey(Question, db_index=True,)
    quiz = models.ForeignKey(Quiz)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.QUESTION_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    e = models.BooleanField(default=False)
    f = models.BooleanField(default=False)
    mark = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100),],
        default=0,
    )

    def __str__(self):
        return str(self.id)


class Me(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_mes'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_index=True,)
    avatar = models.ImageField(upload_to='upload', null=True, blank=True)
    xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        default=0,
    )
    xp_percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    xplevel = models.ForeignKey(XPLevel)
    badges = models.ManyToManyField(Badge, blank=True, related_name='fly_user_badges',)
    courses = models.ManyToManyField(EnrolledCourse, blank=True, related_name='fly_user_enrolled_courses',)
    wants_newsletter = models.BooleanField(default=False)
    wants_goal_notify = models.BooleanField(default=False)
    wants_course_notify = models.BooleanField(default=False)
    wants_resource_notify = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Notification(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_notifications'
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.NOTIFICATION_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    title = models.CharField(max_length=511, null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)
    user = models.ForeignKey(User, db_index=True,)
    xplevel = models.ForeignKey(XPLevel, null=True, blank=True,)
    badge = models.ForeignKey(Badge, null=True, blank=True,)

    def __str__(self):
        return str(self.id)


class Share(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_shares'

    id = models.AutoField(primary_key=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.SHARE_TYPE_OPTIONS,
        default=1,
    )
    user = models.ForeignKey(User, db_index=True,)
    xplevel = models.ForeignKey(XPLevel, null=True, blank=True,)
    badge = models.ForeignKey(Badge, null=True, blank=True,)
    custom_title = models.CharField(max_length=511, null=True, blank=True)
    custom_description = models.CharField(max_length=511, null=True, blank=True)
    custom_url = models.URLField(null=True, blank=True)
    notification_id = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return str(self.id)
