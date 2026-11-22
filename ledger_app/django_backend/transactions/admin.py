from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "txn_id",
        "sender_wallet",
        "receiver_wallet",
        "amount",
        "created_at",
    )
    search_fields = (
        "txn_id",
        "sender_wallet__user__username",
        "receiver_wallet__user__username",
    )
    readonly_fields = (
        "txn_id",
        "sender_wallet",
        "receiver_wallet",
        "amount",
        "remarks",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
