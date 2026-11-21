from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read / update representation of a user. Password is never exposed."""

    # The email is stored as the model's username.
    email = serializers.EmailField(source="username")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "is_active", "date_joined", "last_login")

    def validate_email(self, value):
        qs = User.objects.filter(username__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
