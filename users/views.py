'''
Views for the user API
'''

from .models import User, Tiket
from users.serializers import (
    UserSerializer,
    TiketSerializer,
)
from rest_framework import (
    authentication,
    permissions,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status


class CreateUserView(APIView):
    '''Creating user with Token'''

    def post(self, request):
        '''Create user function.'''

        if request.data['role'] not in ['admin', 'employee']:
            return Response('Role does not match: employee or admin')

        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token = Token.objects.create(user=user)
        return Response({'data':serializer.data,'status':status.HTTP_201_CREATED,'Token':token.key})


class TiketView(APIView):
    '''To create a tiket.'''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        '''Create tiket function'''

        user = User.objects.get(username=request.user)

        if user.role == 'admin' and User.objects.get(username=request.data['assignedTo']):
            serializer = TiketSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            tiket = Tiket.objects.get(title= serializer.data['title'])
            return Response({'Ticket ID':tiket.id, 'status':status.HTTP_201_CREATED})

        else:
            return Response("Only admins can raise tiket!")


class GetTokenView(APIView):
    '''Get token for existing users.'''

    def post(self, request):
        """Find user in db and return token"""

        try:
            user = User.objects.get(username=request.data['username'])
            token = Token.objects.get(user=user)
            return Response({'Token':token.key})

        except User.DoesNotExist:
            return Response("Username is Invalid")
