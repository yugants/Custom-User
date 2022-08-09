'''Serializer for User Model'''

from django.contrib.auth import (
    get_user_model,
)
from .models import User
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


# class AuthTokenSerailizer(serializers.Serializer):
#     '''Serializer for the user auth token.'''

#     username = serializers.CharField()
#     role = serializers.CharField()

#     def validate(self, attr):
#         '''Validate and authenticate the user.'''

#         username = attr.get('username')

#         user = User.objects.get(username=username)

#         if not user:
#             msg = _('Unable to authenticate with username.')
#             raise serializers.ValidationError(msg, code='aunthorization')

#         attr['user'] = user
#         return attr