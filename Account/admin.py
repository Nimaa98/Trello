from django.contrib import admin
from .models import User 

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ('username' ,'email','phone_number','create_at')
    list_filter = ('create_at',)
    search_fields = ('username',)



