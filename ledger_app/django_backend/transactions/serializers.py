from typing import override

from rest_framework import serializers

from .models import Transaction
from .services import create_transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "txn_id",
            "sender_wallet",
            "receiver_wallet",
            "amount",
            "remarks",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("txn_id", "created_at", "updated_at")

    @override
    def create(self, validated_data):
        return create_transaction(
            sender_wallet=validated_data["sender_wallet"],
            receiver_wallet=validated_data["receiver_wallet"],
            amount=validated_data["amount"],
            remarks=validated_data.get("remarks"),
        )

    def update(self, instance, validated_data):
        if "remarks" in validated_data:
            instance.remarks = validated_data["remarks"]
            instance.save(update_fields=["remarks", "updated_at"])
        return instance


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "txn_id",
            "sender_wallet",
            "receiver_wallet",
            "amount",
            "remarks",
            "created_at",
        )
        read_only_fields = fields
