from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    password_changed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user