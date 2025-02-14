from django.db import models
from django.conf import settings
from Core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from Account.models import User
from Core.models import Image


# Create your models here.


class Workspace(BaseModel):


    Workspace_Typs = [('personal','Personal'),('team','Team'),]

    name = models.CharField(_('Name'),max_length=255)
    type = models.CharField(_('Type'),max_length=100,choices=Workspace_Typs)
    description = models.TextField(_('Description'),blank=True, null=True)
    owner = models.ForeignKey(User,verbose_name=_('Owner'),on_delete=models.CASCADE,related_name='owned_workspaces')
    image = models.ForeignKey(Image,verbose_name=_('Image'),on_delete=models.SET_NULL,blank=True , null=True)


    def __str__(self):
        return self.name
    

    class Meta:
        unique_together = ('owner', 'name')
        verbose_name = _('Workspace')
        verbose_name_plural = _('Workspaces')






class WorkspaceUser(BaseModel):
    workspace = models.ForeignKey(Workspace,verbose_name=_('WorkSpace'),on_delete=models.CASCADE,related_name='workspaceusers')
    user = models.ForeignKey(User,verbose_name=_('User'),on_delete=models.CASCADE,related_name='usersworkspace')


    def __str__(self):
            return f"{self.user.username} in {self.workspace.name}"
    

    class Meta:
        unique_together = ('workspace', 'user')
        verbose_name = _('WorkspaceUser')
        verbose_name_plural = _('WorkspaceUsers')

   
    

    
    

class Board(BaseModel):
    title = models.CharField(_('Title'),max_length=100)
    visibility = models.BooleanField(_('Visibility'),default=True)
    image = models.ForeignKey(Image,verbose_name=_('Image'),on_delete=models.SET_NULL,null=True , blank=True)
    workspace = models.ForeignKey(Workspace,verbose_name=_('WorkSpace'),on_delete=models.CASCADE,related_name='boards')

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = _('Board')
        verbose_name_plural = _('Boards')
    
    



class Project(BaseModel):
    title = models.CharField(_('Title'),max_length=100)
    deadline = models.DateField(null=True, blank=True)
    image = models.ForeignKey(Image,verbose_name=_('Image'),on_delete=models.SET_NULL,null=True , blank=True)
    board = models.ForeignKey(Board,verbose_name=_('Board'),on_delete=models.CASCADE,related_name='projects',null=True, blank=True)
    workspace = models.ForeignKey(Workspace,verbose_name=_('Workspace'),on_delete=models.CASCADE,related_name='projects')
    admin = models.ForeignKey(WorkspaceUser,verbose_name=_('Admin'),on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
    





class Role(BaseModel):

    Access_Level_choices = [('level 1','1'),('level 2','2'),('level 3','3'),]

    access_level = models.CharField(_('Access Level'),max_length=50,choices=Access_Level_choices,default='1')
    user = models.ForeignKey(WorkspaceUser,verbose_name=_('User'),on_delete=models.CASCADE,related_name='role')

    def __str__(self):
        return f'{self.user.username}-{self.access_level}'
    
    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')






class Task(BaseModel):
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'),null=True, blank=True)
    start_time = models.DateField(_('Start Time'),null=True, blank=True)
    end_time = models.DateField(_('End Time'),null=True, blank=True)
    delivery_time = models.DateField(_('Delivery Time'))

    status = models.CharField(_('Status'), max_length=50,choices=[('todo','ToDo'),
    ('doing','Doing'),('suspend','Suspend'),('done','Done')], default='todo')

    label = models.CharField(_('Label'), max_length=100,null=True,blank=True)
    project = models.ForeignKey(Project,verbose_name=_('Project'),on_delete=models.CASCADE,related_name='tasks',null=True,blank=True)
    user = models.ForeignKey(Role,verbose_name=_('User') , on_delete=models.SET_NULL,null=True,blank=True,related_name='task')
    workspace = models.ForeignKey(Workspace,verbose_name=_('Workspace'),on_delete=models.CASCADE,related_name='tasks')
    file = models.FileField(_('File'),upload_to='files/', null=True, blank=True,default=None)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')