from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


# Create your views here.


class UserView(viewsets.ModelViewSet):

    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer
