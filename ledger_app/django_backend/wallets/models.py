from django.conf import settings
from django.db import models


class Wallet(models.Model):
    """Exactly one wallet per user (created automatically in User.save())."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # PROTECT - prevents deletion of the user if the wallet is deleted
        related_name="wallet",
    )
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # auto_now_add vs auto_now - auto_now_add is set only once, when the object is created
    # auto_now is set on every save

    class Meta:
        db_table = "wallets"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0), name="wallet_balance_non_negative"
            ),
        ]

    def __str__(self):
        return f"Wallet<{self.user_id}> {self.balance}"
