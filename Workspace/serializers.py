from rest_framework import serializers
from .models import Workspace,Board,Project,Task,Role,WorkspaceUser
from Account.serializers import UserSerializer
from Account.models import User
from Core.models import Image
from datetime import date , datetime



class ImageSerializer:

    image = serializers.SerializerMethodField(read_only=True)

    def get_image(self,obj):
        return obj.image.url if obj.image else None


class WorkspaceUserSerializer(serializers.ModelSerializer):


    username = serializers.CharField(source='user.username', read_only=True)

    workspace_name = serializers.CharField(source='workspace.name', read_only=True)

    workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.all(),write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),write_only=True)



    class Meta:
        model = WorkspaceUser
        fields = ("id","workspace","user","workspace_name","username","create_at")



class RoleSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source = 'user.user.username',read_only =True,default="-")
    user = serializers.PrimaryKeyRelatedField(queryset=WorkspaceUser.objects.all(),write_only=True)

    def validate_access_level(self,value):

        if value not in ['level 1','1','level 2','2','level 3','3']:
            raise serializers.ValidationError("only these these access levels are avalable for users:['level 1','1','level 2','2','level 3','3']")
        return value

    class Meta:
        model = Role
        fields = ("id","access_level","username","user","create_at")



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id","title","start_time","end_time","delivery_time","status","create_at")


class TaskDetailSerializer(serializers.ModelSerializer):

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("title must have at least one letter")
        return value


    def validate_start_time(self, value):
        if value < date.today():
            raise serializers.ValidationError("start time must be in future.")
        return value

    

    def validate_delivery_time(self,value):
        if value < date.today():
            raise serializers.ValidationError("delivery time must be in future.")
        
        return value
    

    def validate(self,data):

        instance = getattr(self,'instance',None)


        start_time = data.get("start_time",instance.start_time if instance else None)

        delivery_time = data.get("delivery_time",instance.delivery_time if instance else None)
        
        status = data.get("status",instance.status if instance else None)


        if delivery_time and start_time and delivery_time < start_time:
            raise serializers.ValidationError("delivery time can not be before start time.")


        if status in ["done","Done"]:
            end_time = date.today()

            if start_time and end_time < start_time:
                raise serializers.ValidationError("end_time can not be before start time.")
            
            if delivery_time and delivery_time < end_time:
                raise serializers.ValidationError("end time can not be before delivery time.")
                      
        return data

    

    def validate_status(self,value):
        Status_Type = ['todo','ToDo','doing','Doing','suspend','Suspend','done','Done']
        if value not in Status_Type:
            raise serializers.ValidationError("invalid status. choose from this list:['todo','doing','suspend','done']")
        return value




    def get_access_level(self,obj):
        if obj.user:
            return obj.user.access_level
        else:
            return None

    access_level = serializers.SerializerMethodField(read_only=True)


    USER = serializers.CharField(source = 'user.user.user.username',read_only =True,default="-")
    user = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(),write_only=True, required=False, allow_null=True)


    project_name = serializers.CharField(source = "project.title",read_only=True,default="-")
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(),write_only=True,required=False, allow_null=True)

    workspace_name = serializers.CharField(source = 'workspace.name', read_only =True)
    workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.all(),write_only=True)

    file = serializers.FileField(required=False, allow_null=True,use_url=True)

    end_time = serializers.DateField(read_only =True)


    class Meta:
        model = Task
        fields = ("id","title", "description","start_time","end_time",
                  "delivery_time","status","label","project","USER","user","access_level",
                  "workspace_name","workspace","project_name","project","file","create_at")






class ProjectSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Project
        fields = ("id","title","image","create_at")


class ProjectDetailSerializer(serializers.ModelSerializer,ImageSerializer):

    tasks = TaskSerializer(many=True, read_only=True)



    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("title must have at least one letter")
        return value



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
    
    
    

    admin_name = serializers.CharField(source = 'admin.user.username',read_only =True,default="-")
    admin = serializers.PrimaryKeyRelatedField(queryset=WorkspaceUser.objects.all(),write_only=True, required=False, allow_null=True)


    board_name = serializers.CharField(source = "board.title",read_only=True,default="-")
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(),write_only=True,required=False, allow_null=True)

    workspace_name = serializers.CharField(source = 'workspace.name', read_only =True)
    workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.all(),write_only=True)


    class Meta:
        model = Project
        fields = ("id","title","workspace_name","workspace","board_name","board","admin_name","admin","image","admin","total_tasks",
                  "completed_tasks","in_progress_tasks","remain_tasks","tasks","create_at")





class BoardSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Board
        fields = ("id","title","visibility","image","create_at")


class BoardDetailSerializer(serializers.ModelSerializer,ImageSerializer):
    projects = ProjectSerializer(many=True,read_only=True)

    
    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("title must have at least one letter")
        return value



    total_projects = serializers.SerializerMethodField(read_only=True)

    def get_total_projects(self,obj):
        return obj.projects.count()


    workspace_name = serializers.CharField(source = 'workspace.name', read_only =True)
    workspace = serializers.PrimaryKeyRelatedField(queryset=Workspace.objects.all(),write_only=True)

    class Meta:
        model = Board
        fields = ("id","title","visibility","workspace_name","workspace","total_projects","image","projects","create_at")





class WorkspaceSerializer(serializers.ModelSerializer,ImageSerializer):

    class Meta:
        model = Workspace
        fields = ("id","name","type","image","create_at")



class WorkspaceDetailSerializer(serializers.ModelSerializer,ImageSerializer):


    boards = BoardSerializer(many=True ,read_only=True)

    def validate_name(self,value):
        user = self.context["request"].user
        if Workspace.objects.filter(name=value,owner=user).exists():
            raise serializers.ValidationError("workspace name is already exists.")
        return value


    def validate_type(self,value):
        Workspace_Typs = ['personal','Personal','team','Team']
        if value not in Workspace_Typs:
            raise serializers.ValidationError("you can only choose between personal type and team type for your workspace type")
        return value


    def validate_image(self,value):
        if not Image.objects.filter(id=value).exists() and value!=None:
            raise serializers.ValidationError("invalid Image ID")
        return value
    

    total_users = serializers.SerializerMethodField(read_only=True)
    total_boards = serializers.SerializerMethodField(read_only=True)


    owner = serializers.CharField(source = 'owner.username' ,read_only=True)

    def get_total_users(self,obj):
        return obj.workspaceusers.count() 


    def get_total_boards(self,obj):
        return obj.boards.count()
    



    class Meta:
        model = Workspace
        fields = ("id","name","type","description","owner","image","total_users","total_boards","boards","create_at")




