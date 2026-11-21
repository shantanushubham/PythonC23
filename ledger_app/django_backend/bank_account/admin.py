from django.contrib import admin

from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bank_name", "account_number", "ifsc_code", "account_type")
    list_filter = ("account_type", "bank_name")
    search_fields = ("user__username", "bank_name", "account_number", "ifsc_code")
