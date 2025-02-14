from rest_framework.permissions import BasePermission


class WorkspacePermission(BasePermission):

    def has_permission(self , request ,view):
        if view.action=='list':
            return request.user.is_authenticated and request.user.is_superuser
        
        if view.action == 'create':
            return request.user.is_anonymous or request.user.is_superuser
        
        
        return request.user.is_authenticated 