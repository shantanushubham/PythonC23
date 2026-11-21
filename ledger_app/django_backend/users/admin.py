from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # The username field is the email address.
    list_display = ("username", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name")
