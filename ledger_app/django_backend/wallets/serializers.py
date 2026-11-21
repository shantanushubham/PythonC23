from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.username", read_only=True)

    class Meta:
        model = Wallet
        fields = ("id", "email", "balance", "created_at", "updated_at")
        # Wallets are created by the system and balances only change through
        # ledger transactions, never directly through this API.
        read_only_fields = fields
