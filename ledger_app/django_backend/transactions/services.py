from decimal import Decimal

from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError

from wallets.models import Wallet

from .models import Transaction


def _apply_transfer(sender, receiver, amount: Decimal):
    if sender.balance < amount:
        raise ValidationError(
            {"amount": "Insufficient balance in the sender wallet."}
        )
    sender.balance -= amount
    receiver.balance += amount
    sender.save(update_fields=["balance", "updated_at"])
    receiver.save(update_fields=["balance", "updated_at"])


@db_transaction.atomic
def create_transaction(
    *,
    sender_wallet,
    receiver_wallet,
    amount,
    remarks=None,
):
    """
    Create a transfer.
    """

    _apply_transfer(sender_wallet, receiver_wallet, amount)

    return Transaction.objects.create(
        sender_wallet=sender_wallet,
        receiver_wallet=receiver_wallet,
        amount=amount,
        remarks=remarks,
    )

