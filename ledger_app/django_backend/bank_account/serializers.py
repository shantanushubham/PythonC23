from decimal import Decimal

from rest_framework import serializers

from .models import BankAccount, BankTransaction
from .services import create_bank_transaction


class UpperCaseCharField(serializers.CharField):
    """Trims and upper-cases input *before* validators run."""

    # to_internal_value is called before any validators are run.
    # Valiidators are rules that are used to validate the data.
    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()


class BankAccountSerializer(serializers.ModelSerializer):
    ifsc_code = UpperCaseCharField(max_length=11)

    class Meta:
        model = BankAccount
        fields = (
            "id",
            "account_holder_name",
            "bank_name",
            "account_number",
            "ifsc_code",
            "account_type",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    # validate is called after all fields are validated on an individual level.
    # It is used to validate the data on a global level.
    def validate(self, attrs):

        # Situation 1: New Bank Account
            # self.instance is None
        # Situation 2: Updating Existing Bank Account
            # self.instance is not None

        # self.instance is the object that is already in the database and is used only during update scenario.

        # Get the request sent by the client from context.
        request = self.context["request"]

        # Get IFSC Code and Account Number from the request. If they are not present, get them from the instance.
        ifsc = attrs.get("ifsc_code", getattr(self.instance, "ifsc_code", None))
        number = attrs.get(
            "account_number", getattr(self.instance, "account_number", None)
        )
        # query = SELECT * FROM bank_account WHERE user_id = request.user.id AND ifsc_code = ifsc AND account_number = number
        qs = BankAccount.objects.filter(
            user=request.user, ifsc_code=ifsc, account_number=number
        )
        if self.instance:
            # If the instance is not None, we need to exclude the current instance from the queryset.]
            # query.append(AND id != instance.pk)
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "You have already added this bank account."
            )
        return attrs


class BankTransactionSerializer(serializers.ModelSerializer):
    txn_id = serializers.UUIDField(source="pk", read_only=True)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2, write_only=True)
    remarks = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, default=None, write_only=True
    )
    sender_wallet = serializers.IntegerField(
        source="transaction.sender_wallet_id", read_only=True, allow_null=True
    )
    receiver_wallet = serializers.IntegerField(
        source="transaction.receiver_wallet_id", read_only=True, allow_null=True
    )

    class Meta:
        model = BankTransaction
        fields = (
            "txn_id",
            "bank_account",
            "direction",
            "status",
            "amount",
            "remarks",
            "sender_wallet",
            "receiver_wallet",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "txn_id",
            "sender_wallet",
            "receiver_wallet",
            "created_at",
            "updated_at",
        )

    def validate_amount(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_bank_account(self, value):
        if value.user_id != self.context["request"].user.id:
            raise serializers.ValidationError("Bank account not found.")
        return value

    def validate(self, attrs):
        if self.instance is not None:
            return attrs
        status = attrs.get("status", BankTransaction.Status.COMPLETED)
        if status not in (
            BankTransaction.Status.PENDING,
            BankTransaction.Status.COMPLETED,
        ):
            raise serializers.ValidationError(
                {"status": "New bank transactions must be pending or completed."}
            )
        attrs["status"] = status
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # amount/remarks live on the linked Transaction row.
        data["amount"] = f"{instance.transaction.amount:.2f}"
        data["remarks"] = instance.transaction.remarks
        return data

    def create(self, validated_data):
        amount = validated_data.pop("amount")
        remarks = validated_data.pop("remarks", None)
        return create_bank_transaction(
            user=self.context["request"].user,
            bank_account=validated_data["bank_account"],
            amount=amount,
            direction=validated_data["direction"],
            remarks=remarks,
            status=validated_data.get("status", BankTransaction.Status.COMPLETED),
        )

    def update(self, instance, validated_data):
        raise serializers.ValidationError(
            "Bank transactions cannot be updated. Create a new one instead."
        )
