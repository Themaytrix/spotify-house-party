from django.contrib import admin
from .models import Newuser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserAdminConfig(UserAdmin):
    ordering=('-start_date')
    list_display = ('email','username')
    fieldsets = ((None,{'fields':('email','username')}))
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields': ('email','username','password')
        })
    )


admin.site.register(Newuser)




