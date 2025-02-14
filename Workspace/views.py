from rest_framework import status, generics, viewsets , serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from .serializers import (WorkspaceSerializer,WorkspaceDetailSerializer,
                        BoardSerializer,BoardDetailSerializer,ProjectSerializer,
                        ProjectDetailSerializer,TaskSerializer,
                        TaskDetailSerializer,RoleSerializer,
                        WorkspaceUserSerializer)

from rest_framework.permissions import AllowAny
from django.db import connection
from .models import Workspace,Board,Project,Task,Role,WorkspaceUser
from django.shortcuts import get_object_or_404
from .permission import WorkspacePermission
from django.core.exceptions import ValidationError

# Create your views here.



class CustomView(viewsets.GenericViewSet):

    lookup_field = 'id'

    def get_object(self):
        return  get_object_or_404(self.get_queryset(),id=self.kwargs['id'])
    




class WorkspaceView(CustomView,viewsets.ModelViewSet):
    
    #lookup_field = 'id'
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Workspace.objects.filter(owner=self.request.user)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_serializer_class(self):

        serializer_class = WorkspaceDetailSerializer
        if self.action == 'list':
            serializer_class = WorkspaceSerializer

        return serializer_class

    

class WorkspaceUserView(CustomView,viewsets.ModelViewSet):
    
    #lookup_field = 'id'
    permission_classes = [AllowAny]
    serializer_class = WorkspaceUserSerializer
    queryset = WorkspaceUser.objects.all()



class BoardView(CustomView,viewsets.ModelViewSet):
    

    #lookup_field = 'id'
    queryset = Board.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):

        serializer_class = BoardDetailSerializer
        if self.action == 'list':
            serializer_class = BoardSerializer

        return serializer_class
    
class ProjectView(CustomView,viewsets.ModelViewSet):
    

    #lookup_field = 'id'
    queryset = Project.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):

        serializer_class = ProjectDetailSerializer
        if self.action == 'list':
            serializer_class = ProjectSerializer

        return serializer_class
    

class TaskView(CustomView,viewsets.ModelViewSet):
    

    #lookup_field = 'id'
    queryset = Task.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):

        serializer_class = TaskDetailSerializer
        if self.action == 'list':
            serializer_class = TaskSerializer

        return serializer_class
    

class RoleView(CustomView,viewsets.ModelViewSet):
    

    #lookup_field = 'id'
    queryset = Role.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RoleSerializer
        

