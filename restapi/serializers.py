from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import UserProfile
from restapi.models import Blog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     return User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])


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
        # instance.user = validated_data.get('user', instance.user)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.location = validated_data.get('location', instance.location)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.save()
        return instance
