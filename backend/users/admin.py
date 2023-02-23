from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .models import Follow


class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'email', 'username', 'is_staff']
    list_filter = ['email', 'username', ]


@register(Follow)
class FollowAdmin(admin.ModelAdmin):
    autocomplete_fields = ('author', 'user')


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
