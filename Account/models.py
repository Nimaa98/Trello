from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from Core.models import BaseModel 
from django.urls import reverse

# Create your models here.

class User(BaseModel , AbstractUser):
     
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True )
    birthday = models.DateField(_('Birthday') , null=True , blank=True)
    bio = models.CharField(_('Biography') , max_length=300 , blank=True)
    email = models.EmailField(_("Email"), max_length=254)
    profile_image = models.ForeignKey('Core.Image' , on_delete= models.SET_DEFAULT ,
                                        null=True , blank=True ,
                                        related_name= 'user_image',
                                        default= None)
   



    class Meta:
            
        verbose_name = _('User')
        verbose_name_plural = _('Users')




    

