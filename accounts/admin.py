from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.

USER  = get_user_model()
@admin.register(USER)
class CustomUserAdmin(UserAdmin):  

    model = USER  

    list_display = ('email', 'is_staff', 'is_active',)  
    list_filter = ('email', 'is_staff', 'is_active',)  
    fieldsets = (  
        (None, {'fields': ('username', 'password')}),  
        ('Personal Information', {'fields':('email','first_name','last_name','date_joined')}),
        ('Permissions', {'fields': ('groups','user_permissions','is_staff', 'is_active','is_superuser')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('username','email', 'password1', 'password2', 'is_staff', 'is_active')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()