from rest_framework import serializers

from .models import BankAccount


class UpperCaseCharField(serializers.CharField):
    """Trims and upper-cases input *before* validators run."""

    def to_internal_value(self, data):
        return super().to_internal_value(data).upper()


class BankAccountSerializer(serializers.ModelSerializer):
    ifsc_code = UpperCaseCharField(
        max_length=11,
        validators=BankAccount._meta.get_field("ifsc_code").validators,
    )

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
        # The owner always comes from the request, never from the payload, and
        # the (user, ifsc, account_number) uniqueness is checked in validate().
        validators = []

    def validate(self, attrs):
        request = self.context["request"]
        ifsc = attrs.get("ifsc_code", getattr(self.instance, "ifsc_code", None))
        number = attrs.get(
            "account_number", getattr(self.instance, "account_number", None)
        )
        qs = BankAccount.objects.filter(
            user=request.user, ifsc_code=ifsc, account_number=number
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "You have already added this bank account."
            )
        return attrs
