from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import ImageUpload
from api.models import BannedDomain
from api.models import BannedIP
from api.models import BannedWord
from api.models import ResourceLink
from api.models import SavingsGoal
from api.models import CreditGoal
from api.models import FinalGoal
from api.models import Badge
from api.models import XPLevel
from api.models import Course
from api.models import Quiz
from api.models import Question
from api.models import EnrolledCourse
from api.models import QuizSubmission
from api.models import QuestionSubmission
from api.models import Me
from api.models import Notification
from api.models import Share


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100,style={'placeholder': 'Email'})
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('upload_id', 'upload_date', 'image', 'user',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        # Validate to ensure the user is not using an email which is banned in
        # our system for whatever reason.
        banned_domains = BannedDomain.objects.all()
        for banned_domain in banned_domains:
            if value.count(banned_domain.name) > 1:
                raise serializers.ValidationError("Email is using a banned domain.")
        return value


class BannedDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedDomain
        fields = ('id','name','banned_on','reason',)


class BannedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedIP
        fields = ('id','address','banned_on','reason',)


class BannedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedWord
        fields = ('id','text','banned_on','reason',)


class ResourceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLink
        fields = ('id','created','title','url','type',)


class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = ('id', 'user', 'goal_type', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'amount', 'times', 'period',)


class CreditGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditGoal
        fields = ('id', 'user', 'goal_type', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'points', 'times', 'period',)


class FinalGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalGoal
        fields = ('id', 'user', 'goal_type', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'amount', 'for_want', 'for_other_want',)

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'created', 'type', 'icon', 'colour', 'level', 'title', 'title_en', 'title_es', 'title_fr', 'description', 'description_en', 'description_es', 'description_fr', 'has_xp_requirement', 'required_xp',)


class XPLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPLevel
        fields = ('id', 'created', 'title', 'num', 'min_xp', 'max_xp',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'type', 'created', 'image', 'title', 'summary', 'description', 'title_en', 'summary_en', 'description_en', 'title_es', 'summary_es', 'description_es', 'title_fr', 'summary_fr', 'description_fr', 'video_url', 'duration', 'awarded_xp', 'has_prerequisites', 'prerequisites',)


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'created', 'course', 'title', 'description', 'title_en', 'description_en', 'title_es', 'description_es', 'title_fr', 'description_fr',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'created', 'quiz', 'num', 'text', 'type', 'a', 'b', 'c', 'd', 'f', 'a_en', 'b_en', 'c_en', 'd_en', 'f_en', 'a_es', 'b_es', 'c_es', 'd_es', 'f_es', 'a_fr', 'b_fr', 'c_fr', 'd_fr', 'f_fr', 'a_is_correct', 'b_is_correct', 'c_is_correct', 'd_is_correct', 'e', 'e_is_correct', 'f_is_correct',)


class EnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledCourse
        fields = ('id', 'created', 'user', 'course', 'finished', 'is_finished', 'final_mark',)


class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubmission
        fields = ('id', 'created', 'user', 'course', 'finished', 'is_finished', 'final_mark',)


class QuestionSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSubmission
        fields = ('id', 'created', 'user', 'quiz', 'type', 'question', 'a', 'b', 'c', 'd', 'e', 'f', 'mark',)


class MeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    num = serializers.IntegerField(source='xplevel.num', read_only=True)
    min_xp = serializers.IntegerField(source='xplevel.min_xp', read_only=True)
    max_xp = serializers.IntegerField(source='xplevel.max_xp', read_only=True)
    class Meta:
        model = Me
        fields = ('id', 'created', 'user', 'avatar', 'xp', 'xp_percent', 'xplevel', 'badges', 'courses', 'wants_newsletter', 'wants_goal_notify', 'wants_course_notify', 'wants_resource_notify', 'num', 'min_xp', 'max_xp', 'username', 'first_name', 'last_name', 'email', 'date_joined')


class NotificationSerializer(serializers.ModelSerializer):
    xplevel_num = serializers.IntegerField(source='xplevel.num', read_only=True)
    xplevel_title = serializers.CharField(source='xplevel.title', read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'type', 'title', 'description', 'user', 'xplevel', 'badge', 'xplevel_num', 'xplevel_title',)


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ('id', 'created', 'type', 'user', 'xplevel', 'badge', 'custom_title', 'custom_description', 'custom_url', 'notification_id',)
