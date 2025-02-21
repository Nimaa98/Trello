from rest_framework import permissions
from .models import Workspace,WorkspaceUser,Board,Project,Task,Role
from django.shortcuts import get_object_or_404
import uuid
from Account.models import User





class WorkspacePermission(permissions.BasePermission):


    def has_permission(self, request,view):
        if request.method == "POST":
            return request.user.is_authenticated 
        
        return True



    def has_object_permission(self , request ,view,obj):
        
        
        
        if request.user == obj.owner:
            return True
        
        if request.method in permissions.SAFE_METHODS:

            is_member = WorkspaceUser.objects.filter(workspace=obj, user=request.user).exists()

            return is_member 


class WorkspaceUserPermission(permissions.BasePermission):
    

    def has_permission(self, request,view):
        workspace_id = request.data.get("workspace")
        user_id = request.data.get("user")
        
        
        if view.action == "create":
            try:
                workspace_uuid = uuid.UUID(str(workspace_id))
                workspace = Workspace.objects.filter(id = workspace_id).first()

                #user_uuid = uuid.UUID(str(user_id))
                #user = User.objects.filter(id = user_id).first()

            except ValueError:
                return False
            
            
            if not workspace:
                return False

            return request.user.is_authenticated and workspace.owner == request.user
        
        return True



    def has_object_permission(self , request ,view,obj):
        
        
        
        if request.user == obj.workspace.owner:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            is_member = WorkspaceUser.objects.filter(workspace=obj.workspace, user=request.user).exists()
            return is_member 
        
        


class BoardPermission(permissions.BasePermission):
    

    def has_permission(self, request,view):
        workspace_id = request.data.get("workspace")
        
        
        if view.action == "create":
            try:
                workspace_uuid = uuid.UUID(str(workspace_id))
                workspace = Workspace.objects.filter(id = workspace_id).first()

            except ValueError:
                return False
            
            
            if not workspace:
                return False

            return request.user.is_authenticated and workspace.owner == request.user
        
        return True



    def has_object_permission(self , request ,view,obj):
        
        
        
        if request.user == obj.workspace.owner:
            return True

        if request.method in permissions.SAFE_METHODS:

            is_member = WorkspaceUser.objects.filter(workspace=obj.workspace, user=request.user).exists()
            return is_member 
        
        


class ProjectPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        workspace_id = request.data.get("workspace")
        workspaceuser_id = request.data.get("admin")
        board_id = request.data.get("board")

        try:
            workspace_uuid = uuid.UUID(str(workspace_id)) if workspace_id else None
            workspace = Workspace.objects.filter(id=workspace_id).first() if workspace_id else None
            
            workspaceuser_uuid = uuid.UUID(str(workspaceuser_id)) if workspaceuser_id else None
            workspaceuser = WorkspaceUser.objects.filter(id=workspaceuser_id).first() if workspaceuser_id else None

            board_uuid = uuid.UUID(str(board_id)) if board_id else None
            board = Board.objects.filter(id=board_id).first() if board_id else None

        except ValueError:
            return False  

        main_condition = request.user.is_authenticated and (workspace and workspace.owner == request.user)

        if view.action == "create":


            return (
                main_condition
                and (not workspaceuser or workspaceuser.workspace == workspace)
                and (not board or board.workspace == workspace)
            )
        
        
        if view.action in ["update", "partial_update"]:
            
            
            
            obj = view.get_object()
            workspace = obj.workspace
            admin = obj.admin.user if obj.admin else None
            

            main_condition = request.user.is_authenticated and (workspace and workspace.owner == request.user) or request.user == admin

            return (
                main_condition
                and (not workspaceuser or workspaceuser.workspace == workspace)
                and (not board or board.workspace == workspace)
            )

        return True

    def has_object_permission(self, request, view, obj):
        is_member = WorkspaceUser.objects.filter(workspace=obj.workspace, user=request.user).exists()

        admin = obj.admin.user if obj.admin else None

        if request.method in permissions.SAFE_METHODS:
        
            return is_member or request.user == obj.workspace.owner

        if view.action in ["update", "partial_update"]:

            return request.user == obj.workspace.owner or admin

        if view.action == "destroy":
            return request.user == obj.workspace.owner

        return False



class RolePermission(permissions.BasePermission):
    

    def has_permission(self, request,view):
        workspaceuser_id = request.data.get("user")
        
        
        if view.action == "create":
            try:
                workspaceuser_uuid = uuid.UUID(str(workspaceuser_id))
                workspaceuser = WorkspaceUser.objects.filter(id = workspaceuser_id).first()

            except ValueError:
                return False
            
            
            if not workspaceuser:
                return False

            return request.user.is_authenticated and workspaceuser.workspace.owner == request.user
        
        return True



    def has_object_permission(self , request ,view,obj):
        workspace = obj.user.workspace
        
        is_member = WorkspaceUser.objects.filter(workspace=workspace, user=request.user).exists()
        
        if request.method in permissions.SAFE_METHODS:

            return is_member or request.user == obj.user.workspace.owner
        
        return request.user == obj.user.workspace.owner




class TaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        workspace_id = request.data.get("workspace")
        role_id = request.data.get("user")
        project_id = request.data.get("project")

        try:
            workspace_uuid = uuid.UUID(str(workspace_id)) if workspace_id else None
            workspace = Workspace.objects.filter(id=workspace_id).first() if workspace_id else None

            role_uuid = uuid.UUID(str(role_id)) if role_id else None
            role = Role.objects.filter(id=role_id).first() if role_id else None

            project_uuid = uuid.UUID(str(project_id)) if project_id else None
            project = Project.objects.filter(id=project_id).first() if project_id else None

        except ValueError:
            return False  

        main_condition = request.user.is_authenticated and (workspace and workspace.owner == request.user)

        if view.action == "create":


            return (
                main_condition
                and (not role or role.user.workspace == workspace)
                and (not project or project.workspace == workspace)
            )
        
        if view.action in ["update", "partial_update"]:

            
           
            obj = view.get_object()
            workspace = obj.workspace
            project_admin = obj.project.admin.user if obj.project and obj.project.admin else None
            

            
            main_condition = request.user.is_authenticated and (
                workspace and workspace.owner == request.user) or request.user== project_admin or self.check_user_permisson(request,obj)

            
            return (
                main_condition
                and (not role or role.user.workspace == workspace)
                and (not project or project.workspace == workspace)
            )

        return True


    def has_object_permission(self, request, view, obj):
        is_member = WorkspaceUser.objects.filter(workspace=obj.workspace, user=request.user).exists()

        project_admin = obj.project.admin.user if obj.project and obj.project.admin else None

        if request.method in permissions.SAFE_METHODS:
        
            return is_member or request.user == obj.workspace.owner

       
        if view.action in ["update", "partial_update"]:
            return request.user == obj.workspace.owner  or project_admin or obj.user

        if view.action == "destroy":
            return request.user == obj.workspace.owner

        return False
    
    def check_user_permisson(self,request,obj):

        file = request.data.get("file")
        status = request.data.get("status")
        delivery_time = request.data.get("delivery_time")

        

        access_level = obj.user.access_level
        user = obj.user.user.user
        
        
        if obj.user and request.user == user:
         
            if file:
                return True
            
            if status and access_level in ["level 2","2", "level 3","3"]:
                return True
            
            if delivery_time and access_level in ["level 3","3"]:
                
                return True    
        
        return False


