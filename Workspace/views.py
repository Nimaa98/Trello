from rest_framework import status, generics, viewsets , serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
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
from django.db.models import Q ,Count
from .models import Workspace,Board,Project,Task,Role,WorkspaceUser
from django.shortcuts import get_object_or_404
from .permission import WorkspacePermission ,WorkspaceUserPermission, BoardPermission ,ProjectPermission, RolePermission,TaskPermission
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# Create your views here.



class ValidateID(ViewSetMixin):

    lookup_field = 'id'
    
class WorkspaceView(ValidateID,viewsets.ModelViewSet):
    
    
    permission_classes = [WorkspacePermission]
    
    
    def get_object(self):
        return super().get_object()
    

    def get_queryset(self):
        user= self.request.user
        if not user.is_authenticated:
            return Workspace.objects.none()
        
        return Workspace.objects.filter(Q(owner=user) | Q(workspaceusers__user=user)).distinct()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_serializer_class(self):

        serializer_class = WorkspaceDetailSerializer
        if self.action == 'list':
            serializer_class = WorkspaceSerializer

        return serializer_class

    

class WorkspaceUserView(ValidateID,viewsets.ModelViewSet):
    
    
    permission_classes = [WorkspaceUserPermission]
    serializer_class = WorkspaceUserSerializer
    

    def get_queryset(self):
        
        user= self.request.user
        if not user.is_authenticated:
           return WorkspaceUser.objects.none()
        
        return WorkspaceUser.objects.filter(Q(workspace__owner=user) | Q(workspace__workspaceusers__user=user)).distinct()
    #.values("workspace__id","workspace__name","workspace__owner").annotate(count=Count("workspace__id"))
    
    


class BoardView(ValidateID,viewsets.ModelViewSet):
    
    
    permission_classes = [BoardPermission]

    def get_serializer_class(self):

        serializer_class = BoardDetailSerializer
        if self.action == 'list':
            serializer_class = BoardSerializer

        return serializer_class
    
    def get_queryset(self):
        
        user= self.request.user
        if not user.is_authenticated:
           return WorkspaceUser.objects.none()
        
        return Board.objects.filter(Q(workspace__owner=user) | Q(workspace__workspaceusers__user=user)).distinct()


    
class ProjectView(ValidateID,viewsets.ModelViewSet):
    
    
    permission_classes = [ProjectPermission]

    def get_serializer_class(self):

        serializer_class = ProjectDetailSerializer
        if self.action == 'list':
            serializer_class = ProjectSerializer

        return serializer_class


    def get_queryset(self):
        
        user= self.request.user
        if not user.is_authenticated:
           return WorkspaceUser.objects.none()
        
        return Project.objects.filter(Q(workspace__owner=user) | Q(workspace__workspaceusers__user=user)).distinct()
    

class TaskView(ValidateID,viewsets.ModelViewSet):
    
    permission_classes = [TaskPermission]


    def get_serializer_class(self):

        serializer_class = TaskDetailSerializer
        if self.action == 'list':
            serializer_class = TaskSerializer

        return serializer_class
    

    def get_queryset(self):
        
        user= self.request.user
        if not user.is_authenticated:
           return WorkspaceUser.objects.none()
        
        return Task.objects.filter(Q(workspace__owner=user) | Q(workspace__workspaceusers__user=user)).distinct()
    

class RoleView(ValidateID,viewsets.ModelViewSet):
    

    
    permission_classes = [RolePermission]
    serializer_class = RoleSerializer

    def get_queryset(self):
        
        user= self.request.user
        if not user.is_authenticated:
           return WorkspaceUser.objects.none()
        
        return Role.objects.filter(Q(user__workspace__owner=user) | Q(user__workspace__workspaceusers__user=user)).distinct()
        

