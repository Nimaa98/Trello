from django.contrib import admin
from .models import Workspace,WorkspaceUser,Board,Project,Task,Role

# Register your models here.

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):

    list_display = ('name' , 'type','owner', 'description', 'create_at')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(WorkspaceUser)
class WorkspaceUserdmin(admin.ModelAdmin):

    list_display = ('workspace' , 'user', 'create_at')
    list_filter = ('workspace',)
    search_fields = ('user__username','user__email',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):

    list_display = ('title' , 'visibility', 'workspace', 'create_at')
    list_filter = ('workspace',)
    search_fields = ('title',)




@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title' , 'deadline', 'board', 'admin','create_at')
    list_filter = ('board',)
    search_fields = ('title',)




@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = ('user' , 'access_level', 'create_at')
    list_filter = ('access_level',)
    search_fields = ('user__username','user__email',)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ('title' , 'delivery_time', 'status','label','get_project','get_user', 'create_at')
    list_filter = ('status','project','user',)
    search_fields = ('title',)


    def get_project(self,obj):
        if obj.project:
            return obj.project.title 
        else:
            return "-"
    
    def get_user(self,obj):
        if obj.user:
            return obj.user.user.username
        else:
            return "-"
    
    get_project.short_description = "Project"
    get_user.short_description = "User"

    





    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'status', 'label',
                       ('description',),)
        }),
        ('Time Details', {
            'fields': ('start_time', 'end_time','delivery_time',)
        }),
        ('Relations', {
            'fields': ('project', 'user','file',)
        }),

    )



