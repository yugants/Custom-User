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


class TiketFilterView(APIView):
    '''Tikets filter methods'''

    def get(self, request):
        '''Return tickets according to parameters'''

        if self.request.query_params.get('status', None):
                tikets = Tiket.objects.filter(status = request.query_params['status'])
                tiketserializer =  TiketSerializer(tikets, many=True)

        elif self.request.query_params.get('title', None):
                tikets = Tiket.objects.get(title = request.query_params['title'])
                tiketserializer =  TiketSerializer(tikets)

        elif self.request.query_params.get('priority', None):
                tikets = Tiket.objects.filter(priority = request.query_params['priority']).order_by('priority')
                tiketserializer =  TiketSerializer(tikets, many=True)

        else:
                tiket = Tiket.objects.all()
                tiketserializer = TiketSerializer(tiket, many=True)

        return Response({'Tickets':tiketserializer.data})


class CloseTiketView(APIView):
    '''Ticket Closing endpoint'''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        '''Only admins and ticket owner
        can close the ticket'''

        try:
            id = self.request.data['id']
            tiket = Tiket.objects.get(id = id)


        except Tiket.DoesNotExist:
            return Response('Incorrect ticket id.')

        '''Only close ticket if not higher priority
        ticket is pending.'''

        user = User.objects.get(username=request.user)

        if user.role == 'admin' or user.username == tiket.assignedTo:

            tikets = Tiket.objects.filter(assignedTo=tiket.assignedTo)

            if tiket.priority =='high':
                    tiket.status = 'close'
                    tiket.save()
                    return Response({"Ticket Closed High priority":tiket.status})

            for i in tikets:
                if i.id == id:
                    continue

                elif i.priority == 'high' and i.status == 'open':
                    return Response("Cannot close, another tiket with \
                    high priority pending")

                elif i.priority == 'medium' and tiket.priority =='low' and i.status == 'open':
                    return Response("Cannot close, another tiket with \
                    high priority pending")

                elif tiket.priority == 'medium':
                    tiket.status = 'close'
                    tiket.save()
                    return Response({"Ticket Closed Medium priority":tiket.status})

                elif tiket.priority == 'low':
                    tiket.status = 'close'
                    tiket.save()
                    return Response({"Ticket Closed Low priority":tiket.status})

        else:
            return Response("Only and admins and ticket owners can close ticket.")


class TiketDeleteView(APIView):
    '''To delete tickets'''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        '''Only admins can delete.'''

        try:
            tiket = Tiket.objects.get(id=request.data['id'])

        except Tiket.DoesNotExist:
            return Response('Incorrect ticket id.')

        if request.user.role == "admin" and tiket:
            tiket.delete()
            return Response('deleted successfully')

        else:
            return Response("Invalid Request")
