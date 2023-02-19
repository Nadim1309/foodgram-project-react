from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class MyAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("email", "first_name")


admin.site.unregister(Group)
