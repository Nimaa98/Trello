from django.contrib import admin
from .models import Image

# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = ('name','Image' ,'alt_text', 'create_at')
    list_filter = ('create_at',)
    search_fields = ('name',)