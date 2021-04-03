from django.contrib import admin
from api.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from django.db import models


# custom django admin pannel view 

class UserAdminConfig(UserAdmin):
    model = User
    # admin can search by these fields
    search_fields = ('email', 'last_name', 'first_name')

    # admin can use filter with these fields
    list_filter = ('email', 'last_name', 'first_name', 'is_active', 'is_staff')

    # admin can sort the user
    ordering = ('-start_date',)
    list_display = ('email', 'last_name', 'first_name',
                    'is_active', 'is_staff','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_teacher','is_student','is_superuser')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff','is_teacher','is_student')}
         ),
    )


admin.site.register(User, UserAdminConfig)