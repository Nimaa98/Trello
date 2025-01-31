from django.db import models 
from django.utils.translation import gettext_lazy as _
import uuid



# Create your models here.

class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


    

class Image(BaseModel):

    alt_text = models.CharField(_('Alternative Text'), max_length=50 , blank=True, null=True)
    Image = models.ImageField(_('Image'), upload_to='images/' )
    
    class Meta:

        verbose_name = _('Image')
        verbose_name_plural = _('Images')

