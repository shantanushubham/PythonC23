from django.contrib import admin

from .models import BankAccount, BankTransaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bank_name", "account_number", "ifsc_code", "account_type")
    list_filter = ("account_type", "bank_name")
    search_fields = ("user__username", "bank_name", "account_number", "ifsc_code")


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ("pk", "bank_account", "direction", "status", "created_at")
    list_filter = ("direction", "status")
    search_fields = ("pk", "bank_account__account_number", "bank_account__user__username")
    readonly_fields = (
        "transaction",
        "bank_account",
        "direction",
        "status",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
