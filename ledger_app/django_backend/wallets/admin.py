from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("user", "balance", "created_at", "updated_at")

    def has_add_permission(self, request):
        return False  # created automatically with the user

    def has_delete_permission(self, request, obj=None):
        return False
