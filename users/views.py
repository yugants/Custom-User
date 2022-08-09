'''
Views for the user API
'''

from .models import User
from users.serializers import (
    UserSerializer,
)
from rest_framework import (
    generics,
    authentication,
    permissions,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework import status


class CreateUserView(APIView):
    '''Creating user with Token'''

    def post(self, request):
        '''Create user function.'''

        serializer = UserSerializer(data = request.data)   # request.data gives the data from user to serializer
        if not serializer.is_valid():                               # is_valid() checks if the data format given is valid or not?
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token = Token.objects.create(user=user)
        return Response({'data':serializer.data,'status':status.HTTP_201_CREATED,'Token':token.key})


class ManageUserView(generics.RetrieveUpdateAPIView):
    '''Manage the authenticated user.'''

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user


# class CreateUserView(generics.CreateAPIView):
#     '''Create a new user in the system'''

#     serializer_class = UserSerializer


# class CreateTokenView(ObtainAuthToken):
#     '''Create a new auth token for user.'''

#     serializer_class = AuthTokenSerailizer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
