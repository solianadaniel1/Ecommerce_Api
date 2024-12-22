from django.contrib import admin
from django.contrib.auth import get_user_model

user = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']  
    search_fields = ['username', 'email']
    list_filter = ['username', 'email']  

    
admin.site.register(user, UserAdmin)
