import uuid

from django.db import models


class Transaction(models.Model):
    """A wallet-to-wallet money transfer."""

    txn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Nullable so bank deposits (sender=None) and withdrawals (receiver=None) work.
    sender_wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.PROTECT,
        related_name="sent_transactions",
        null=True,
        blank=True,
    )
    receiver_wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.PROTECT,
        related_name="received_transactions",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    remarks = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0), name="transaction_amount_positive"
            ),
            # Wallet-to-wallet and bank flows both need at least one side set.
            models.CheckConstraint(
                condition=(
                    models.Q(sender_wallet__isnull=False)
                    | models.Q(receiver_wallet__isnull=False)
                ),
                name="transaction_has_at_least_one_wallet",
            ),
            # When both wallets are set, they must be different.
            models.CheckConstraint(
                condition=(
                    models.Q(sender_wallet__isnull=True)
                    | models.Q(receiver_wallet__isnull=True)
                    | ~models.Q(sender_wallet=models.F("receiver_wallet"))
                ),
                name="transaction_wallets_differ",
            ),
        ]

    def __str__(self):
        return f"Txn<{self.txn_id}> {self.amount}"
