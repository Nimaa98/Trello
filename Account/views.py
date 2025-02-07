from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .permission import UserPermission
from rest_framework.permissions import AllowAny
from django.db import connection

# Create your views here.



class UserView(viewsets.ModelViewSet):
    


    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    
    

    def get_object(self):
        #if self.action == 'custom-action':
            #return self.request.user
        return super().get_object()
    

    @action(detail=False , methods=['get','put','patch','delete'] , url_path='custom-action')
    def custom_action(self,request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)


        elif request.method in ['PUT','PATCH']:
            serializer = self.get_serializer(request.user, data = request.data , partial = (request.method == 'PATCH'))
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'DELETE':
            request.user.delete()
            return Response({'message': 'user deleted successfully'} , status=204)
            