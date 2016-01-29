from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import ImageUpload
from api.models import BannedDomain
from api.models import BannedIP
from api.models import BannedWord
from api.models import Goal
from api.models import Badge
from api.models import XPLevel
from api.models import Course
from api.models import Quiz
from api.models import Question
from api.models import EnrolledCourse
from api.models import QuizSubmission
from api.models import QuestionSubmission
from api.models import Me


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
        fields = ('upload_id', 'upload_date', 'is_assigned', 'image', 'user',)


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


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'created', 'was_accomplished', 'user', 'type', 'amount', 'times', 'for_want', 'for_other_want',)


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'created', 'type', 'image', 'level', 'title', 'description', 'has_xp_requirement', 'required_xp',)


class XPLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'created', 'level', 'required_xp',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'created', 'title', 'summary', 'description', 'video_url', 'duration', 'awarded_xp', 'prerequisites',)


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'created', 'course', 'title', 'description',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'created', 'quiz', 'num', 'title', 'description', 'type', 'a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct', 'true_choice', 'false_choice', 'answer',)


class EnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledCourse
        fields = ('id', 'created', 'user', 'course', 'finished', 'is_finished', 'marks',)


class QuizSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubmission
        fields = ('id', 'created', 'user', 'course', 'finished', 'is_finished', 'marks',)


class QuestionSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSubmission
        fields = ('id', 'created', 'user', 'quiz', 'type', 'a', 'b', 'c', 'd', 'e', 'f', 'tf_answer', 'marks',)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Me
        fields = ('id', 'created', 'user', 'avatar', 'level', 'xp', 'badges', 'courses',)

