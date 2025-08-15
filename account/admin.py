from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name','date_joined','last_login' ,'is_admin', 'is_active','is_staff')
    list_display_links = ('email','first_name')
    list_filter = ('is_admin', 'is_active', 'is_staff')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superadmin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin', 'is_superadmin'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
