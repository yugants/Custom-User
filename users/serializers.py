'''Serializer for User Model'''

from django.contrib.auth import (
    get_user_model,
)
from .models import User, Tiket
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for the user object'''

    class Meta:
        model = get_user_model()
        fields = ['username', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        '''Create and return a user.'''

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Update and return user, instance is model'''

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class TiketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tiket
        fields = ['title','assignedTo']
