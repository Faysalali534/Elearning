from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, generics
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import UserProfile
from djoser.serializers import UserCreateSerializer
from learning_material.models import Lesson, Course, EnrollStudent
from restapi.models import Blog
from restapi.google import Google, register_social_user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'last_name', 'password']


class BlogSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    desc = serializers.CharField(max_length=30)

    # automatically invoked when is_valid method is called
    def validate_name(self, value):
        if len(value) <= 4:
            raise serializers.ValidationError('Name too short')
        return value

    def create(self, validate_data):
        return Blog.objects.create(**validate_data)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'location', 'user_type']

    def create(self, validate_data):
        phone = validate_data["phone_number"]
        location = validate_data['location']
        user_type = validate_data['user_type']
        user_data = validate_data.pop('user')
        user = User.objects.create(**user_data)
        profile = UserProfile.objects.create(user=user, phone_number=phone, location=location, user_type=user_type)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', instance.user)
        User.objects.filter(username__exact=instance).update(
            username=user_data['username'],
            first_name=user_data['first_name'],
            email=user_data['email'],
            last_name=user_data['last_name'],
            password=user_data['password']
        )
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.location = validated_data.get('location', instance.location)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.save()
        return instance

    def put(self, instance, validated_data):
        user_data = validated_data.get('user', instance.user)
        return instance


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')


class LoginApiSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials!')

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'Token is invalid or expired'
            )
        if user_data['aud'] != '993340120000-keb638moekcpkivo0v1h8qhqq3rpifs4.apps.googleusercontent.com':
            raise AuthenticationFailed('ops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
