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
    banned_on = models.DateTimeField(auto_now_add=True)
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
    banned_on = models.DateTimeField(auto_now_add=True)
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
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.text)


class ImageUpload(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('upload_date',)
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


class Goal(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_goals'
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    unlocks = models.DateTimeField(null=True,blank=True)
    was_accomplished = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.GOAL_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    
    times = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
    )
    
    period = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=constants.INTERVAL_OPTIONS,
        default=1,
    )
    
    for_want = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        choices=constants.FOR_WANT_OPTIONS,
        default=1,
    )
    for_other_want = models.CharField(max_length=63, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)


class Badge(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_badges'
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=constants.BADGE_TYPE_OPTIONS,
        default=1,
    )
    image = models.ImageField(upload_to='upload', null=True, blank=True)
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
            return XPLevel.objects.get(level=1)
        except XPLevel.DoesNotExist:
            return self.create(
                level=1,
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
    level = models.PositiveSmallIntegerField(
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


class Course(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_courses'
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
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
    prerequisites = models.ManyToManyField("self", blank=True,)
    
    def __str__(self):
        return str(self.id)


class Quiz(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_quizzes'
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course)
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
    quiz = models.ForeignKey(Quiz)
    num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        default=1,
    )
    title = models.CharField(max_length=63, null=True, blank=True)
    description = models.CharField(max_length=511, null=True, blank=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
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

    true_choice = models.CharField(max_length=127, null=True, blank=True,)
    false_choice = models.CharField(max_length=127, null=True, blank=True,)
    answer = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class EnrolledCourse(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'fly_enrolled_courses'
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    finished = models.DateTimeField(null=True, blank=True,)
    is_finished = models.BooleanField(default=False)
    marks = models.FloatField(
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
    user = models.ForeignKey(User)
    course = models.ForeignKey(EnrolledCourse)
    finished = models.DateTimeField(null=True, blank=True,)
    is_finished = models.BooleanField(default=False)
    marks = models.FloatField(
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
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(QuizSubmission)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
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
    tf_answer = models.BooleanField(default=False)
    marks = models.FloatField(
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
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='upload', null=True, blank=True)
    xp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99999)],
        default=0,
        db_index=True,
    )
    xp_percent = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    xplevel = models.ForeignKey(XPLevel)
    badges = models.ManyToManyField(Badge, blank=True, related_name='fly_user_awarded_badges',)
    courses = models.ManyToManyField(EnrolledCourse, blank=True, related_name='fly_user_enrolled_courses',)
    
    def __str__(self):
        return str(self.id)
