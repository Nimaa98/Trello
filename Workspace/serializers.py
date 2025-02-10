from rest_framework import serializers
from .models import Workspace,Board,Project,Task,Role
from Account.serializers import UserSerializer


class ImageSerializer:

    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self,obj):
        return obj.image.url if obj.image else None




class WorkspaceSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Workspace
        fields = ("id","name","type","image","create_at")


class WorkspaceDetailSerializer(serializers.ModelSerializer,ImageSerializer):


    total_users = serializers.SerializerMethodField(read_only=True)
    total_boards = serializers.SerializerMethodField(read_only=True)


    def get_total_users(self,obj):
        return obj.workspaceusers.count() 


    def get_total_boards(self,obj):
        return obj.boards.count()
    



    class Meta:
        model = Workspace
        fields = ("id","name","type","description","image","total_users","total_boards","create_at")







class BoardSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Board
        fields = ("id","title","visibility","workspace","image","create_at")


class BoardDetailSerializer(serializers.ModelSerializer,ImageSerializer):

    total_projects = serializers.SerializerMethodField(read_only=True)

    def get_total_projects(self,obj):
        return obj.projects.count()


    workspace = serializers.CharField(source = 'workspace.name', read_only =True)

    class Meta:
        model = Board
        fields = ("id","title","visibility","workspace","total_projects","image","create_at")







class ProjectSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Project
        fields = ("id","title","board","image","create_at")



class ProjectDetailSerializer(serializers.ModelSerializer,ImageSerializer):


    total_tasks = serializers.SerializerMethodField(read_only=True)
    completed_tasks = serializers.SerializerMethodField(read_only=True)
    in_progress_tasks = serializers.SerializerMethodField(read_only=True)
    remain_tasks = serializers.SerializerMethodField(read_only=True)
    


    def get_total_tasks(self,obj):
        return obj.tasks.count()
    

    def get_completed_tasks(self,obj):
        return obj.tasks.filter(status='done').count() 
    

    def get_in_progress_tasks (self,obj):
        return obj.tasks.filter(status = 'doing').count() 
    

    def get_remain_tasks(self,obj):
        return obj.tasks.filter(status= 'todo').count() 
    
    
    board = serializers.CharField(source = "board.title",read_only=True,default="-")

    admin = serializers.CharField(source = 'admin.user.username',read_only =True,default="-")


    class Meta:
        model = Project
        fields = ("id","title","deadline","board","image","admin","total_tasks",
                  "completed_tasks","in_progress_tasks","remain_tasks","create_at")







class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id","title","delivery_time","status","create_at")


class TaskDetailSerializer(serializers.ModelSerializer):

    project = serializers.CharField(source = 'project.title', read_only =True, default="-")

    user = serializers.CharField(source = 'user.user.user.username',read_only =True,default="-")


    class Meta:
        model = Task
        fields = ("id","title", "description","start_time","end_time",
                  "delivery_time","status","label","project","user","file","create_at")
        







class RoleSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source = 'user.user.username',read_only =True,default="-")

    class Meta:
        model = Role
        fields = ("id","access_level","user","create_at")