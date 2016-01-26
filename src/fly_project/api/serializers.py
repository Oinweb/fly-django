from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers

#from api.models.ec.receipt import Receipt
#from api.models.ec.helprequest import HelpRequest
from api.models import ImageUpload
from api.models import BannedDomain
from api.models import BannedIP
from api.models import BannedWord


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