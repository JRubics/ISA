from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class AdminInline(admin.StackedInline):
    model = AdminUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (AdminInline, ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.register(UserRelationship)
admin.site.register(DiscountPointReference)
